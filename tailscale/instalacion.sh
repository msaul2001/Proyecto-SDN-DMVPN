
#!/bin/bash

# Proyecto SDN-DMVPN Dual Hub
# Instalacion de Tailscale en Ubuntu Server

set -e

# Actualizar repositorios
sudo apt update

# Instalar dependencias
sudo apt install -y curl

# Instalar Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Habilitar e iniciar el servicio
sudo systemctl enable --now tailscaled

# Autenticar el dispositivo en la Tailnet
sudo tailscale up

# Mostrar version instalada
tailscale version

# Verificar estado del servicio
sudo systemctl is-active tailscaled
