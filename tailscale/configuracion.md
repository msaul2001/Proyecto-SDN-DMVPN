
# Configuracion del Gateway Tailscale

## Objetivo

Implementar conectividad remota hacia la infraestructura
del proyecto SDN-DMVPN Dual Hub mediante Tailscale.

## Servidor

- Hostname: gw-tailscale
- Sistema operativo: Ubuntu Server
- Version Tailscale: 1.104.6

## Interfaces de red

| Interfaz | Direccionamiento | Funcion |
|---|---|---|
| ens33 | DHCP | Acceso a Internet |
| ens34 | 172.16.0.10/24 | Conexion hacia DMVPN |
| tailscale0 | Asignado por Tailscale | VPN |

## Configuracion de Netplan

La configuracion de red se encuentra disponible en:

[netplan.yaml](configuraciones/netplan.yaml)

## IP Forwarding

Se habilito el reenvio de paquetes IPv4 mediante:

net.ipv4.ip_forward = 1

Archivo de configuracion:

[99-tailscale.conf](configuraciones/99-tailscale.conf)

## Validaciones realizadas

- Servicio tailscaled activo.
- Servicio habilitado al iniciar el servidor.
- Dispositivos registrados en la Tailnet.
- IP Forwarding habilitado.
- Comunicacion UDP disponible.
- Servidor DERP mas cercano: Miami.
- Latencia hacia DERP: 54 ms.

## Seguridad

No se incluyen credenciales, llaves de autenticacion,
direcciones IP publicas ni archivos privados de Tailscale.
