
# Pruebas de conectividad Tailscale

## Objetivo

Validar la comunicacion entre el gateway Tailscale
y los seis routers Cisco del proyecto SDN-DMVPN.

## Subnet Router

- Servidor: gw-tailscale
- Subred anunciada: 172.16.0.0/24
- Interfaz hacia DMVPN: ens34
- IP del gateway: 172.16.0.10/24
- IP Forwarding: habilitado
- SNAT: habilitado
- Netfilter: habilitado

## Resultados de conectividad

| Router | IP | Paquetes recibidos | Perdida | RTT promedio |
|---|---|---|---|---|
| R1 | 172.16.0.1 | 3/3 | 0% | 1.039 ms |
| R2 | 172.16.0.2 | 3/3 | 0% | 1.474 ms |
| R3 | 172.16.0.3 | 3/3 | 0% | 0.889 ms |
| R4 | 172.16.0.4 | 3/3 | 0% | 4.289 ms |
| R5 | 172.16.0.5 | 3/3 | 0% | 1.289 ms |
| R6 | 172.16.0.6 | 3/3 | 0% | 1.431 ms |

## NAT y enrutamiento

Tailscale administra las reglas de NAT mediante
la cadena ts-postrouting y utiliza MASQUERADE
para el trafico marcado por el servicio.

El reenvio de paquetes utiliza la cadena
ts-forward de iptables.

## Conclusion

Se valido exitosamente la comunicacion desde
gw-tailscale hacia los seis routers Cisco,
sin perdida de paquetes.

La validacion de acceso remoto desde otro
dispositivo de la Tailnet se realiza por separado.
