
# Guía de instalación - Proyecto SDN-DMVPN Dual Hub

## Descripción

Esta guía describe el procedimiento para preparar el entorno
de automatización, administración y acceso remoto de la
infraestructura SDN-DMVPN implementada en EVE-NG.

El proyecto integra routers Cisco, Ansible, Flask, Zabbix
y Tailscale.

## Requisitos generales

- Ubuntu Server.
- Python 3.
- Acceso a Internet.
- EVE-NG con Cisco IOL 15.7.
- Acceso SSH a los routers Cisco.
- Usuario con privilegios administrativos.
- Cuenta autorizada en Tailscale.

## 1. Preparación del entorno Python

Clonar el repositorio:

    git clone https://github.com/msaul2001/Proyecto-SDN-DMVPN.git

Ingresar al directorio:

    cd Proyecto-SDN-DMVPN

Instalar los requisitos del sistema:

    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip git

Crear el entorno virtual:

    python3 -m venv venv

Activar el entorno virtual:

    source venv/bin/activate

Instalar las dependencias del proyecto:

    pip install -r requirements.txt

Las dependencias se encuentran documentadas en:

[requirements.txt](requirements.txt)

## 2. Instalación de colecciones Ansible

Desde la raíz del repositorio, ejecutar:

    ansible-galaxy collection install -r ansible/requirements.yml

Las colecciones permiten administrar los equipos Cisco
mediante los playbooks de automatización.

## 3. Configuración de Ansible Vault

Ingresar al directorio de Ansible:

    cd ansible

Crear el archivo Vault:

    ansible-vault create vars/vault.yml

Utilizar el archivo vault.example.yml como referencia.

La PSK configurada debe coincidir con la utilizada en
los routers Cisco para establecer las asociaciones IPsec.

Por seguridad, el archivo Vault real no se incluye
en el repositorio.

## 4. Configuración y validación del inventario

El inventario contiene los routers R1 a R7 del proyecto.

| Router | Dirección IP | Función |
|---|---|---|
| R1 | 172.16.0.1 | Hub primario |
| R2 | 172.16.0.2 | Hub secundario |
| R3 | 172.16.0.3 | Spoke Mazatenango |
| R4 | 172.16.0.4 | Spoke Suchitepéquez |
| R5 | 172.16.0.5 | Spoke Zacapa |
| R6 | 172.16.0.6 | Spoke Retalhuleu |
| R7 | 172.16.0.7 | Nueva sucursal |

Desde el directorio ansible, consultar el inventario:

    ansible-inventory --graph

Las configuraciones y archivos de automatización
se encuentran disponibles en:

[Directorio Ansible](ansible/)

## 5. Automatización de sucursales

### 5.1. Simulación de alta de R7

Desde el directorio ansible:

    ansible-playbook playbooks/alta_sucursal.yml --ask-pass --ask-vault-pass --check -f 1

El parámetro --check permite realizar una simulación
en los módulos compatibles, sin aplicar los cambios
previstos a la infraestructura.

### 5.2. Alta de sucursal

    ansible-playbook playbooks/alta_sucursal.yml --ask-pass --ask-vault-pass -f 1

### 5.3. Baja de sucursal

    ansible-playbook playbooks/baja_sucursal.yml --ask-pass -f 1

Las operaciones de alta y baja modifican la
infraestructura y deben ejecutarse únicamente
con autorización y respaldos previos.

### 5.4. Playbooks disponibles

- alta_sucursal.yml
- baja_sucursal.yml
- backup_routers.yml

Los playbooks actuales administran específicamente R7.

## 6. Instalación y configuración del portal web

Regresar a la raíz del repositorio:

    cd ..

Mantener activo el entorno virtual de Python.

Configurar la autenticación del portal:

    python webapp/setup_auth.py

Iniciar la aplicación:

    python webapp/app.py

El portal escucha en:

    http://127.0.0.1:5000

Para acceder remotamente se utiliza un túnel SSH
hacia el servidor donde se ejecuta la aplicación.

El portal permite administrar las operaciones
de automatización mediante los playbooks de Ansible.

### Funciones principales

- Alta de sucursal.
- Baja de sucursal.
- Simulación de configuración.
- Consulta de estado.
- Respaldo de configuraciones.
- Guardado de configuraciones.

El código fuente se encuentra disponible en:

[Directorio Webapp](webapp/)

## 7. Consideraciones de la implementación

- Se requiere acceso a la red underlay 172.16.0.0/24.
- Los routers deben contar con acceso SSH.
- Se requiere un usuario con privilegio 15 en Cisco.
- Las claves reales no se incluyen en GitHub.
- Los playbooks actuales administran específicamente R7.
- Los indicadores del portal son estáticos.
- El registro de hosts en Zabbix se realiza por separado.
- El portal corresponde a una implementación de laboratorio.

## 8. Instalación y configuración de Tailscale

Para proporcionar acceso remoto a la infraestructura
SDN-DMVPN implementada en EVE-NG, se utiliza un servidor
Ubuntu denominado gw-tailscale, configurado como Subnet Router.

### 8.1. Requisitos

- Ubuntu Server.
- Dos interfaces de red.
- Acceso a Internet.
- Cuenta autorizada en Tailscale.
- Acceso a la red underlay de EVE-NG.

### 8.2. Configuración de red

| Interfaz | Direccionamiento | Función |
|---|---|---|
| ens33 | DHCP | Acceso a Internet |
| ens34 | 172.16.0.10/24 | Conexión con EVE-NG |
| tailscale0 | Asignado por Tailscale | Acceso remoto VPN |

La configuración de referencia se encuentra en:

[netplan.yaml](tailscale/configuraciones/netplan.yaml)

### 8.3. Instalación de Tailscale

Desde la raíz del repositorio, en el servidor
gw-tailscale, ejecutar:

    bash tailscale/instalacion.sh

Durante la instalación se debe autenticar el
servidor dentro de la Tailnet correspondiente.

La versión utilizada en el proyecto es 1.104.6.

### 8.4. Configuración de IP Forwarding

El servidor requiere el reenvío de paquetes IPv4:

    net.ipv4.ip_forward = 1

El archivo de configuración se encuentra en:

[99-tailscale.conf](tailscale/configuraciones/99-tailscale.conf)

### 8.5. Configuración como Subnet Router

Una vez configuradas las interfaces de red y
autenticado Tailscale, ejecutar:

    bash tailscale/configuraciones/enrutamiento.sh

El script realiza las siguientes configuraciones:

- Habilitación de IP Forwarding.
- Anuncio de la subred 172.16.0.0/24.
- Habilitación de SNAT.

Tailscale administra automáticamente las reglas
de NAT y forwarding mediante Netfilter.

### 8.6. Aprobación de la subred

1. Ingresar a la consola administrativa de Tailscale.
2. Seleccionar el dispositivo gw-tailscale.
3. Acceder a la configuración de rutas anunciadas.
4. Aprobar la subred 172.16.0.0/24.
5. Autorizar los dispositivos correspondientes.

Los clientes Linux que requieran utilizar las rutas
anunciadas deben habilitar su aceptación:

    sudo tailscale set --accept-routes=true

### 8.7. Documentación complementaria

- [README de Tailscale](tailscale/README.md)
- [Instalación](tailscale/instalacion.sh)
- [Configuración del gateway](tailscale/configuracion.md)
- [Netplan](tailscale/configuraciones/netplan.yaml)
- [IP Forwarding](tailscale/configuraciones/99-tailscale.conf)
- [Enrutamiento](tailscale/configuraciones/enrutamiento.sh)

## 9. Laboratorio EVE-NG y routers Cisco

La infraestructura virtualizada utiliza Cisco IOL 15.7
y está compuesta por dos hubs y cinco sucursales,
incluyendo R7 para la demostración de alta automatizada.

### Tecnologías implementadas

- DMVPN Dual Hub.
- mGRE y NHRP.
- IKEv2 e IPsec.
- BGP IPv4 e IPv6.
- Redes LAN dual stack.

Los archivos correspondientes se encuentran en:

- [Laboratorio EVE-NG](eveng/)
- [Configuraciones Cisco](routers/)

Las imágenes de Cisco IOL deben obtenerse por
los medios autorizados correspondientes.

## 10. Monitoreo mediante Zabbix

La infraestructura utiliza Zabbix 7.0 para el
monitoreo de los routers Cisco mediante SNMPv3 authPriv.

Se utiliza la plantilla Cisco IOS by SNMP y
configuraciones personalizadas de monitoreo.

### Indicadores principales

- Disponibilidad.
- CPU y memoria.
- Latencia y pérdida de paquetes.
- Tráfico de interfaces.
- Estado DMVPN.
- Estado BGP IPv4 e IPv6.
- Asociaciones IPsec.

Se implementaron 22 triggers personalizados:

- 8 correspondientes a BGP IPv4.
- 8 correspondientes a BGP IPv6.
- 6 correspondientes a IPsec.

El registro de los routers en Zabbix se realiza
manualmente como parte de esta implementación.

Consultar los archivos de monitoreo en:

[Directorio Zabbix](zabbix/)

## 11. Seguridad

El repositorio no debe contener información sensible
relacionada con la infraestructura.

No publicar:

- Contraseñas de los servidores.
- Credenciales de los routers Cisco.
- Claves PSK reales de IPsec.
- Credenciales SNMPv3.
- Archivos Ansible Vault reales.
- Tokens de autenticación.
- Llaves de autenticación Tailscale.
- Llaves privadas SSH.
- Archivos privados de Tailscale.
- Credenciales del portal web.

Utilizar los archivos de ejemplo y el archivo
.gitignore para proteger la información sensible.

## 12. Documentación general

Para consultar la arquitectura, direccionamiento,
componentes, limitaciones y matriz de cumplimiento
del proyecto, acceder al documento principal:

[README principal del proyecto](README.md)
