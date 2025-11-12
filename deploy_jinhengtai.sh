#!/bin/bash
set -euo pipefail

# --- 配置 --- #
# 服务的名称，用于 systemd
SERVICE_NAME="jinhengtai.service"
# 后端代码所在的目录 (相对于项目根目录)
BACKEND_DIR="backend"
# 为此应用分配一个独立的端口
APP_PORT=8001
# Python 虚拟环境的名称
VENV_NAME="venv"

# --- 脚本开始 --- #

echo "--- Starting deployment script for Jinhengtai ---"

cd "$BACKEND_DIR"

# 1. 创建或更新 Python 虚拟环境
echo "Setting up Python virtual environment..."
if [ ! -d "$VENV_NAME" ]; then
  python3 -m venv "$VENV_NAME"
fi

# 2. 安装/更新依赖
echo "Installing/updating Python dependencies..."
source "$VENV_NAME/bin/activate"
# 确保 pip 是最新的
pip install --upgrade pip
# 从 requirements.txt 安装依赖
pip install -r requirements.txt
deactivate

# 3. 创建或更新 systemd 服务文件
echo "Creating/Updating systemd service file: /etc/systemd/system/$SERVICE_NAME"

# 注意：WorkingDirectory 指向的是 backend 目录
# ExecStart 指向虚拟环境中的 uvicorn
cat << EOF | sudo tee /etc/systemd/system/$SERVICE_NAME > /dev/null
[Unit]
Description=Jinhengtai FastAPI Backend Service
After=network.target

[Service]
User=root
# 将工作目录设置为 backend 目录
WorkingDirectory=$(pwd)
# 执行命令：使用虚拟环境中的 python 启动 uvicorn
ExecStart=$(pwd)/$VENV_NAME/bin/uvicorn app.main:app --host 0.0.0.0 --port $APP_PORT
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 4. 重新加载 systemd 并重启服务
echo "Reloading systemd and restarting the service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

# 5. 检查服务状态
echo "Checking service status..."
sleep 3 # 等待几秒钟让服务启动
sudo systemctl status $SERVICE_NAME --no-pager

echo "--- Deployment script finished successfully! ---"
