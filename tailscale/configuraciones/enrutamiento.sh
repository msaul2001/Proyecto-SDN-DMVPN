
#!/bin/bash

# Proyecto SDN-DMVPN Dual Hub
# Configuracion de Tailscale como Subnet Router

set -e

# Habilitar IP Forwarding
echo "net.ipv4.ip_forward = 1" | \
sudo tee /etc/sysctl.d/99-tailscale.conf

sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

# Anunciar la subred de los routers Cisco
sudo tailscale set --advertise-routes=172.16.0.0/24

# Mantener SNAT habilitado
sudo tailscale set --snat-subnet-routes=true

# Validar configuracion
tailscale status
ip route
ip route show table 52

# Validar reglas NAT y Forwarding
sudo iptables -t nat -S
sudo iptables -S FORWARD

# IMPORTANTE:
# Aprobar la ruta 172.16.0.0/24 desde
# la consola administrativa de Tailscale.
