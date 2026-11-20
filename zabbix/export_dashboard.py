import json
import urllib.request
from getpass import getpass
from pathlib import Path

url = "http://127.0.0.1/zabbix/api_jsonrpc.php"

def api(method, params, token=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    headers = {"Content-Type": "application/json-rpc"}

    if token:
        headers["Authorization"] = "Bearer " + token

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.load(response)

    if "error" in result:
        raise RuntimeError(result["error"])

    return result["result"]

usuario = input("Usuario Zabbix: ")
password = getpass("Contrasena Zabbix: ")

token = api("user.login", {
    "username": usuario,
    "password": password
})

try:
    dashboards = api("dashboard.get", {
        "output": "extend",
        "selectPages": "extend",
        "search": {"name": "NMS-SDN"}
    }, token)

    if not dashboards:
        raise SystemExit("No se encontro el dashboard.")

    archivo = Path.home() / "zabbix-export/dashboard.json"

    archivo.write_text(
        json.dumps(dashboards, indent=4, ensure_ascii=False)
    )
    archivo.chmod(0o600)

    for dashboard in dashboards:
        print("Dashboard:", dashboard["name"])
        print("Paginas:", len(dashboard["pages"]))
        print("Widgets:", sum(
            len(p["widgets"]) for p in dashboard["pages"]
        ))

    print("Archivo generado:", archivo)

finally:
    api("user.logout", [], token)
