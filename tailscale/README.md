
# Tailscale - SDN DMVPN Dual Hub

## Descripcion

Tailscale permite el acceso remoto a la infraestructura
virtualizada en EVE-NG mediante una VPN basada en WireGuard.

Se implemento un servidor Ubuntu denominado gw-tailscale,
configurado como Subnet Router para proporcionar acceso
a la red de los routers Cisco del proyecto.

## Arquitectura

- Gateway: gw-tailscale
- Version Tailscale: 1.104.6
- Interfaz de Internet: ens33 (DHCP)
- Interfaz hacia DMVPN: ens34 (172.16.0.10/24)
- Subred anunciada: 172.16.0.0/24
- IP Forwarding: habilitado
- SNAT: habilitado

## Archivos del repositorio

- [Instalacion de Tailscale](instalacion.sh)
- [Documentacion de configuracion](configuracion.md)
- [Configuracion Netplan](configuraciones/netplan.yaml)
- [Configuracion IP Forwarding](configuraciones/99-tailscale.conf)
- [Configuracion Subnet Router](configuraciones/enrutamiento.sh)

## Orden de implementacion

1. Instalar Tailscale.
2. Autenticar el servidor en la Tailnet.
3. Configurar las interfaces de red mediante Netplan.
4. Habilitar IP Forwarding.
5. Configurar Tailscale como Subnet Router.
6. Aprobar la subred anunciada desde la consola
   administrativa de Tailscale.

## Seguridad

Las credenciales, llaves de autenticacion y archivos
privados de Tailscale no se incluyen en el repositorio.
