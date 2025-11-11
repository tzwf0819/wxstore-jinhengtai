#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/opt/jinhengtai-backend"
COMPOSE_FILE="${PROJECT_ROOT}/docker-compose.yml"

if ! command -v docker &>/dev/null; then
  echo "[ERROR] Docker 未安装，请先安装 Docker" >&2
  exit 1
fi

if ! command -v docker compose &>/dev/null && ! command -v docker-compose &>/dev/null; then
  echo "[ERROR] docker compose 未安装，请安装 docker compose 或 docker-compose" >&2
  exit 1
fi

echo "[INFO] 创建部署目录结构"
mkdir -p "${PROJECT_ROOT}/deploy/nginx/conf.d"
mkdir -p "${PROJECT_ROOT}/deploy/certs"
mkdir -p "${PROJECT_ROOT}/deploy/logs"
mkdir -p "${PROJECT_ROOT}/deploy/tmp"
mkdir -p "${PROJECT_ROOT}/app"

cat <<'EOF' >"${PROJECT_ROOT}/deploy/nginx/conf.d/default.conf"
server {
    listen 80;
    server_name _;
    return 444;
}
EOF

echo "[INFO] 部署 Certbot 挂载目录"
mkdir -p /var/www/certbot
chown -R root:root /var/www/certbot

if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
  echo "[ERROR] 未发现 docker-compose.yml" >&2
  exit 1
fi

echo "[INFO] 使用 Docker Compose 启动服务"
cd "${PROJECT_ROOT}"
if command -v docker compose &>/dev/null; then
  docker compose pull
  COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose up -d --build --remove-orphans
else
  docker-compose pull
  COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up -d --build --remove-orphans
fi

echo "[INFO] 服务已启动"
