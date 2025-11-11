#!/usr/bin/env bash
set -euo pipefail

DOMAIN="jinhengtai.yidasoftware.xyz"
EMAIL="admin@yidasoftware.xyz"
NGINX_CONF_DIR="/opt/jinhengtai-backend/deploy/nginx/conf.d"
CERT_ROOT="/opt/jinhengtai-backend/deploy/certs"

if ! command -v certbot &>/dev/null; then
  echo "[ERROR] certbot 未安装，请先安装 certbot" >&2
  exit 1
fi

certbot certonly \
  --webroot -w /var/www/certbot \
  --email "${EMAIL}" \
  --agree-tos \
  --non-interactive \
  -d "${DOMAIN}" \
  -d "api.${DOMAIN}"

cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem "${CERT_ROOT}/fullchain.pem"
cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem "${CERT_ROOT}/privkey.pem"

systemctl reload nginx
