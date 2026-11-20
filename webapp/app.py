from flask import (
    Flask, render_template, jsonify,
    request, session, redirect, url_for, abort
)
from werkzeug.security import check_password_hash
from pathlib import Path
from functools import wraps
from datetime import timedelta
import subprocess
import secrets
import hmac
import json

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "webapp/auth.json") as f:
    auth = json.load(f)

app = Flask(__name__)
app.secret_key = auth["secret_key"]

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)

def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]

def validar_csrf():
    esperado = session.get("csrf_token", "")
    recibido = request.form.get("csrf_token", "")
    if not esperado or not hmac.compare_digest(esperado, recibido):
        abort(400)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("logged_in") is not True:
            if request.path.startswith("/api/"):
                return jsonify({"error": "No autorizado"}), 401
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

@app.after_request
def proteger_respuesta(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        validar_csrf()

        usuario = request.form.get("username", "")
        password = request.form.get("password", "")

        if (
            usuario == auth["username"]
            and check_password_hash(auth["password_hash"], password)
        ):
            session.clear()
            session["logged_in"] = True
            session["username"] = usuario
            session.permanent = True
            return redirect(url_for("index"))

        error = "Usuario o contraseña incorrectos."

    return render_template(
        "login.html",
        error=error,
        csrf_token=csrf_token()
    )

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    validar_csrf()
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        csrf_token=csrf_token()
    )

@app.route("/api/inventario")
@login_required
def inventario():
    try:
        resultado = subprocess.run(
            [
                str(BASE_DIR / "venv/bin/ansible-inventory"),
                "--list"
            ],
            cwd=BASE_DIR / "ansible",
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )

        datos = json.loads(resultado.stdout)
        routers = datos.get("_meta", {}).get("hostvars", {})

        return jsonify({
            "success": True,
            "total": len(routers),
            "routers": [
                {
                    "nombre": nombre,
                    "ip": variables.get("ansible_host")
                }
                for nombre, variables in sorted(routers.items())
            ]
        })

    except Exception:
        return jsonify({
            "success": False,
            "error": "No se pudo consultar el inventario"
        }), 500


from ansible_engine import ejecutar, OPERACIONES, REQUIERE_VAULT

@app.route("/api/ejecutar", methods=["POST"])
@login_required
def ejecutar_operacion():

    validar_csrf()

    operacion = request.form.get("operacion", "")
    ssh_password = request.form.get("ssh_password", "")
    vault_password = request.form.get("vault_password", "")

    if operacion not in OPERACIONES:
        return jsonify({
            "success": False,
            "output": "Operacion no permitida."
        }), 400

    if not ssh_password:
        return jsonify({
            "success": False,
            "output": "Debe ingresar la contrasena SSH."
        }), 400

    if operacion in REQUIERE_VAULT and not vault_password:
        return jsonify({
            "success": False,
            "output": "Debe ingresar la contrasena Vault."
        }), 400

    if operacion in {"alta", "baja", "guardar"}:
        if request.form.get("confirmacion") != operacion:
            return jsonify({
                "success": False,
                "output": "Operacion no confirmada."
            }), 400

    success, output = ejecutar(
        operacion,
        ssh_password,
        vault_password
    )

    return jsonify({
        "success": success,
        "output": output
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
