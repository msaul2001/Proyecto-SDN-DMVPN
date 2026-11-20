# Conectividad remota mediante Tailscale

## Objetivo

Permitir la comunicacion entre el controlador Ansible,
el servidor Zabbix y los routers Cisco alojados en EVE-NG,
sin exponerlos directamente a Internet.

## Arquitectura

- EVE-NG sobre VMware Workstation.
- Gateway Ubuntu con dos interfaces de red.
- VMnet8: conexion NAT hacia Internet.
- VMnet4: conexion hacia la red underlay.
- Underlay: 172.16.0.0/24.
- Gateway de administracion: 172.16.0.10.
- Tailscale configurado como subnet router.

## Funcionamiento

El gateway anuncia la red 172.16.0.0/24 mediante
Tailscale. El servidor remoto acepta esta ruta y
puede administrar los routers mediante SSH, SNMPv3
e ICMP.

Esta arquitectura permite ejecutar los playbooks
de Ansible y monitorear los equipos mediante Zabbix
desde una ubicacion remota.
