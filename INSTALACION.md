
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

### 8.3. Instalación

La instalación de Tailscale se realiza mediante
el siguiente script:

[instalacion.sh](tailscale/instalacion.sh)

Desde la raíz del repositorio, ejecutar:

    bash tailscale/instalacion.sh

Durante la instalación se debe autenticar el servidor
dentro de la Tailnet correspondiente.

### 8.4. Configuración del gateway

Configurar las interfaces de red utilizando como
referencia el archivo:

[netplan.yaml](tailscale/configuraciones/netplan.yaml)

Habilitar el reenvío de paquetes IPv4 y configurar
el servidor como Subnet Router mediante:

    bash tailscale/configuraciones/enrutamiento.sh

La subred anunciada corresponde a 172.16.0.0/24,
utilizada por los routers Cisco del proyecto.

El script mantiene SNAT habilitado y permite que
Tailscale administre automáticamente las reglas
de NAT y forwarding.

### 8.5. Aprobación de la subred

1. Ingresar a la consola administrativa de Tailscale.
2. Seleccionar el dispositivo gw-tailscale.
3. Acceder a la configuración de rutas anunciadas.
4. Aprobar la subred 172.16.0.0/24.
5. Autorizar los dispositivos que tendrán acceso
   a la infraestructura del proyecto.

### 8.6. Documentación complementaria

- [README de Tailscale](tailscale/README.md)
- [Configuración del gateway](tailscale/configuracion.md)
- [Script de instalación](tailscale/instalacion.sh)
- [Configuración Netplan](tailscale/configuraciones/netplan.yaml)
- [IP Forwarding](tailscale/configuraciones/99-tailscale.conf)
- [Configuración de enrutamiento](tailscale/configuraciones/enrutamiento.sh)

La implementación fue realizada utilizando
Tailscale versión 1.104.6.

Por seguridad, no se incluyen credenciales,
llaves de autenticación ni archivos privados
de Tailscale dentro del repositorio.
