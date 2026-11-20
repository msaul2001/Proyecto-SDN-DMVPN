from pathlib import Path
from datetime import datetime
from threading import Lock
import pexpect
import os
import re

BASE_DIR = Path(__file__).resolve().parent.parent
BIN = BASE_DIR / "venv/bin"

LOCK = Lock()

OPERACIONES = {
    "alta": "Alta de sucursal R7",
    "baja": "Baja de sucursal R7",
    "simular_alta": "Simulacion de alta R7",
    "simular_baja": "Simulacion de baja R7",
    "validar": "Validacion de R7",
    "backup": "Respaldo de routers",
    "guardar": "Guardar configuraciones"
}

REQUIERE_VAULT = {"alta", "simular_alta"}


def construir_comando(operacion):

    if operacion in ("alta", "simular_alta"):
        args = [
            str(BIN / "ansible-playbook"),
            "playbooks/alta_sucursal.yml",
            "--ask-pass",
            "--ask-vault-pass",
            "-f", "1"
        ]

        if operacion == "simular_alta":
            args.append("--check")

        return args

    if operacion in ("baja", "simular_baja"):
        args = [
            str(BIN / "ansible-playbook"),
            "playbooks/baja_sucursal.yml",
            "--ask-pass",
            "-f", "1"
        ]

        if operacion == "simular_baja":
            args.append("--check")

        return args

    if operacion == "backup":

        import json

        carpeta = BASE_DIR / "backups" / (
            "portal_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        carpeta.mkdir(mode=0o700, exist_ok=False)

        return [
            str(BIN / "ansible"),
            "routers_sdn",
            "-m", "cisco.ios.ios_config",
            "-a", json.dumps({
                "backup": True,
                "backup_options": {
                    "dir_path": str(carpeta)
                }
            }),
            "--ask-pass",
            "-f", "2"
        ]

    if operacion == "validar":
        return [
            str(BIN / "ansible"),
            "R7",
            "-m", "cisco.ios.ios_command",
            "-a", '{"commands":["show ip interface brief",'
                  '"show ipv6 interface brief",'
                  '"show crypto ikev2 sa",'
                  '"show dmvpn",'
                  '"show ip bgp summary",'
                  '"show bgp ipv6 unicast summary"]}',
            "--ask-pass"
        ]

    if operacion == "guardar":
        return [
            str(BIN / "ansible"),
            "routers_sdn",
            "-m", "cisco.ios.ios_config",
            "-a", '{"save_when":"always"}',
            "--ask-pass",
            "-f", "2"
        ]

    raise ValueError("Operacion no permitida")


def ejecutar(operacion, ssh_password, vault_password=""):

    if operacion not in OPERACIONES:
        return False, "Operacion no permitida."

    if not LOCK.acquire(blocking=False):
        return False, "Ya existe una operacion en ejecucion."

    proceso = None
    salida = []

    try:
        comando = construir_comando(operacion)

        entorno = os.environ.copy()
        entorno["ANSIBLE_NOCOLOR"] = "1"
        entorno["ANSIBLE_DISPLAY_ARGS_TO_STDOUT"] = "False"

        proceso = pexpect.spawn(
            comando[0],
            comando[1:],
            cwd=str(BASE_DIR / "ansible"),
            encoding="utf-8",
            codec_errors="replace",
            timeout=600,
            echo=False,
            env=entorno
        )

        intentos = {"ssh": 0, "vault": 0}

        while True:

            evento = proceso.expect([
                r"SSH password:",
                r"Vault password:",
                pexpect.EOF,
                pexpect.TIMEOUT
            ])

            salida.append(proceso.before or "")

            if evento == 0:
                intentos["ssh"] += 1

                if intentos["ssh"] > 1:
                    return False, "Error de autenticacion SSH."

                proceso.sendline(ssh_password)

            elif evento == 1:
                intentos["vault"] += 1

                if intentos["vault"] > 1:
                    return False, "Error de autenticacion Vault."

                proceso.sendline(vault_password)

            elif evento == 2:
                break

            else:
                return False, (
                    "Tiempo de espera agotado. "
                    "Revisar estado de los routers antes de repetir."
                )

        proceso.close()

        texto = "".join(salida)

        texto = re.sub(
            r"\x1b\[[0-9;]*[A-Za-z]",
            "",
            texto
        )

        for clave in (ssh_password, vault_password):
            if clave:
                texto = texto.replace(clave, "[OCULTO]")

        texto = "\n".join(
            linea for linea in texto.splitlines()
            if not re.search(
                r"pre-shared-key|password|secret|dmvpn_psk",
                linea,
                re.IGNORECASE
            )
        )

        exito = proceso.exitstatus == 0

        return exito, texto

    except Exception:
        return False, (
            "Error al ejecutar Ansible. "
            "Revisar el servidor antes de repetir la operacion."
        )

    finally:
        try:
            if proceso is not None and proceso.isalive():
                proceso.close(force=True)
        finally:
            LOCK.release()
