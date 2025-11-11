#!/bin/bash
# This script creates and enables a systemd service for the FastAPI application.
set -euo pipefail

# --- Configuration ---
SERVICE_NAME="jinhengtai-backend"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PROJECT_DIR="/opt/cloudbase"
BACKEND_DIR="${PROJECT_DIR}/backend"
VENV_DIR="${PROJECT_DIR}/venv"
# This should be the user that owns the project files and runs the service.
# We assume 'sa' based on your previous input.
SERVICE_USER="sa"

echo "--- [1/3] Creating systemd service file at ${SERVICE_FILE} ---"

# Create the service file content using a 'here document'
sudo tee ${SERVICE_FILE} > /dev/null <<EOF
[Unit]
Description=Jinhengtai Mall Backend FastAPI Service
# Start this service after the network is available
After=network.target

[Service]
# Set the user and group for the service
User=${SERVICE_USER}
Group=${SERVICE_USER}

# Set the working directory for the application
WorkingDirectory=${BACKEND_DIR}

# The deployment script will create the .env file, systemd will load it here
EnvironmentFile=${BACKEND_DIR}/.env

# The command to start the application, using the Python from the virtual environment
ExecStart=${VENV_DIR}/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

# Restart the service if it fails
Restart=always
RestartSec=10

# Standard output and error logging
StandardOutput=journal
StandardError=journal

[Install]
# Enable this service for the default multi-user target
WantedBy=multi-user.target
EOF

echo "--- [2/3] Reloading systemd daemon and enabling the service ---"
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}

echo "--- [3/3] Service setup complete! ---"
echo "The '${SERVICE_NAME}' service has been created and enabled."
echo "The deployment script will now be able to start/restart it automatically."
