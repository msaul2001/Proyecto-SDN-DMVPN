# Instalacion del proyecto SDN

## 1. Entorno Python

Desde la raiz del repositorio:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## 2. Colecciones Ansible

    ansible-galaxy collection install -r ansible/requirements.yml

## 3. Configurar Ansible Vault

    cd ansible
    ansible-vault create vars/vault.yml

Utilizar vault.example.yml como referencia.
La clave IPsec debe coincidir con la configurada
en los routers del laboratorio.

## 4. Validar inventario

Desde la carpeta ansible:

    ansible-inventory --graph

## 5. Simular alta de R7

    ansible-playbook playbooks/alta_sucursal.yml --ask-pass --ask-vault-pass --check -f 1

## 6. Configurar el portal

Regresar a la raiz del repositorio:

    cd ..
    python webapp/setup_auth.py
    python webapp/app.py

El portal escucha en 127.0.0.1:5000.
Para acceder remotamente utilizar un tunel SSH.

## 7. Consideraciones

- Se requiere conectividad hacia los routers.
- Se requiere acceso SSH con privilegio 15.
- Las claves reales no se incluyen en Git.
- Los playbooks actuales administran especificamente R7.
- Los indicadores del portal son estaticos.
- El registro de hosts en Zabbix se realiza por separado.
- El portal corresponde a una implementacion de laboratorio.
