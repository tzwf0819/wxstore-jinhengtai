#!/bin/bash
# This script provisions a server with Python 3.8+ and MS ODBC Driver 18.
set -euo pipefail

echo '--- [1/2] Starting Server Provisioning ---'

# --- Determine Package Manager ---
if command -v apt-get &>/dev/null; then
    PKG_MANAGER='apt-get'
    PYTHON_PKG='python3.8 python3.8-venv python3.8-dev'
    ODBC_PREREQS='curl gnupg unixodbc-dev'
elif command -v dnf &>/dev/null; then
    PKG_MANAGER='dnf'
    PYTHON_PKG='python38 python38-devel'
    ODBC_PREREQS='curl gnupg unixODBC-devel'
elif command -v yum &>/dev/null; then
    PKG_MANAGER='yum'
    PYTHON_PKG='python38 python38-devel'
    ODBC_PREREQS='curl gnupg unixODBC-devel'
else
    echo 'ERROR: Unsupported package manager (apt, dnf, or yum not found).' >&2
    exit 1
fi

echo "Updating package manager repositories using [${PKG_MANAGER}]..."
sudo ${PKG_MANAGER} update -y

echo "Installing Python 3.8+ and virtual environment package..."
if ! command -v python3.8 &>/dev/null; then
    sudo ${PKG_MANAGER} install -y ${PYTHON_PKG}
fi

echo "Installing Microsoft ODBC Driver 18 for SQL Server..."
if ! odbcinst -q -d -n 'ODBC Driver 18 for SQL Server'; then
    echo "Driver not found, starting installation..."
    sudo ${PKG_MANAGER} install -y ${ODBC_PREREQS}
    
    # Add Microsoft repository key and sources
    curl -sS https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
    if [ "${PKG_MANAGER}" = "apt-get" ]; then
        curl -sS https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
    else # For dnf/yum
        curl -sS https://packages.microsoft.com/config/rhel/8/prod.repo | sudo tee /etc/yum.repos.d/mssql-release.repo
    fi

    sudo ${PKG_MANAGER} update -y
    sudo ACCEPT_EULA=Y ${PKG_MANAGER} install -y msodbcsql18 mssql-tools18
    
    echo "Adding ODBC tools to PATH for this session..."
    export PATH="/opt/mssql-tools18/bin:$PATH"
else
    echo "ODBC Driver 18 for SQL Server is already installed."
fi

echo '--- [2/2] Server Provisioning Finished Successfully! ---'
