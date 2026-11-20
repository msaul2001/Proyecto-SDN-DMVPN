from werkzeug.security import generate_password_hash
from pathlib import Path
from getpass import getpass
import secrets
import json
import os

os.umask(0o077)

archivo = Path(__file__).resolve().parent / "auth.json"

if archivo.exists():
    raise SystemExit("El archivo auth.json ya existe.")

usuario = input("Usuario del portal: ").strip()
password = getpass("Nueva contrasena: ")
confirmacion = getpass("Confirmar contrasena: ")

if not usuario:
    raise SystemExit("Usuario requerido.")

if password != confirmacion or len(password) < 12:
    raise SystemExit("Contrasena invalida.")

datos = {
    "username": usuario,
    "password_hash": generate_password_hash(password),
    "secret_key": secrets.token_hex(32)
}

archivo.write_text(json.dumps(datos, indent=4))
archivo.chmod(0o600)

print("Credenciales creadas correctamente.")
