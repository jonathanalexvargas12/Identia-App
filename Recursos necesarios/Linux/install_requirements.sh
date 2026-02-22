#!/bin/bash

# Script de instalación para Identia App - Linux (Ubuntu/Debian)

echo "============================================================"
echo "🚀 INICIANDO INSTALACIÓN DE RECURSOS PARA IDENTIA APP"
echo "============================================================"

# Actualizar repositorios
sudo apt-get update

# 1. Instalar Python 3.11 y herramientas esenciales
echo "🐍 Instalando Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# 2. Instalar MariaDB (Versión estable)
echo "🗄️ Instalando MariaDB Server..."
sudo apt-get install -y mariadb-server libmariadb-dev
# Iniciar servicio
sudo systemctl start mariadb
sudo systemctl enable mariadb

# 3. Instalar Docker
echo "🐳 Instalando Docker Engine..."
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Añadir repositorio de Docker
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. Configurar permisos de Docker para el usuario actual
sudo usermod -aG docker $USER

# 5. Instalar Gestor de Base de Datos Visual (DBeaver)
echo "📊 Instalando DBeaver (Gestor visual)..."
sudo snap install dbeaver-ce

echo "============================================================"
echo "✅ INSTALACIÓN COMPLETADA"
echo "⚠️ NOTA: Por favor, reinicie su sesión para que los cambios de Docker surtan efecto."
echo "============================================================"