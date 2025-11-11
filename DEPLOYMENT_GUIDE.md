# 微信小程序电商系统部署指南

## 架构概览
- 微信小程序前端调用 FastAPI REST 接口提供的数据服务
- FastAPI 通过 SQLAlchemy 连接本地 MSSQL Server，实现商品、分类、库存与订单逻辑
- Docker Compose 编排 `api`（FastAPI）、`mssql`（SQL Server）、`nginx` 三个服务
- Nginx 暴露 80/443 端口，负责反向代理、HTTPS、路径重写与证书续期
- GitHub Actions 负责单元测试与自动部署脚本触发（可按需扩展）

## 服务拓扑

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  微信小程序端   │ ---> │     Nginx       │ ---> │   FastAPI API   │
│  (用户访问)     │      │ 80/443 反向代理 │      │    (uvicorn)    │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                                │
                                                ▼
                                       ┌─────────────────┐
                                       │   SQL Server    │
                                       │   (MSSQL 2022)  │
                                       └─────────────────┘
```

## 域名与访问入口
- `https://api.jinhengtai.yidasoftware.xyz`：微信小程序及其他客户端直接调用的 API 域名（`app.js` 中的 `apiBaseUrl` 已指向该地址）
- `https://yidasoftware.xyz/jinhengtai/`：主域名下的访问入口，Nginx 会将该前缀下的请求重写后转发给 FastAPI 服务
- `https://yidasoftware.xyz/jinhengtai/docs`：FastAPI Swagger（被动转发）
- `https://yidasoftware.xyz/jinhengtai/openapi.json`：OpenAPI 文档（被动转发）
- `http://152.136.13.33/`：新增的 IP 直连入口，适用于尚未完成域名解析或调试阶段（仅 HTTP，无证书，加密需自行评估）

> 使用 HTTP 直连时，请在第一台主机的反向代理中直接指向 `http://152.136.13.33`，无需再追加 `/jinhengtai` 前缀；若要对外提供 HTTPS，请仍以域名方式访问。

## 服务器目录结构
```
/opt/jinhengtai-backend
├── docker-compose.yml          # Compose 定义文件
├── deploy
│   ├── nginx/conf.d/api.conf   # Nginx 主配置（含域名、路径、证书）
│   ├── certs/                  # 存放 fullchain.pem / privkey.pem
│   ├── logs/                   # Nginx 访问与错误日志
│   ├── tmp/                    # 临时文件（缓存等）
│   └── scripts/
│       ├── setup.sh            # 一键部署/更新脚本
│       └── renew_cert.sh       # Certbot 证书续期脚本
├── backend/                    # FastAPI 应用源码
└── .env                        # API 服务环境变量（需手动创建）
```

## 环境变量与数据库
- SQL Server 位于 `mssql` 容器中，通过 Compose 网络访问，默认 SA 密码存放在 `.env`
- FastAPI 读取 `.env` 中的数据库连接串、JWT 设置等配置（请参考 `backend/app/core/config.py` 注释）
- 如需外部连通 MSSQL，可在宿主机开放 1433，默认 Compose 已做 `1433:1433` 端口映射

## 部署流程（首次或更新）
1. **同步代码**：将最新仓库内容上传到服务器 `/opt/jinhengtai-backend`
2. **准备环境**：确认服务器已安装 Docker 与（新版）`docker compose`/旧版 `docker-compose`
3. **配置变量**：在 `backend/.env` 中补齐数据库、JWT、第三方服务配置
4. **执行脚本**：运行 `sudo bash deploy/scripts/setup.sh`
   - 自动创建目录结构与默认 Nginx 配置
   - 自动执行 `docker compose up -d --build --remove-orphans`
5. **校验服务**：
   - `docker ps` 查看 `jinhengtai-api`、`jinhengtai-nginx`、`jinhengtai-mssql` 均为 `Up`
   - 访问 `https://api.jinhengtai.yidasoftware.xyz/docs` 或 `https://yidasoftware.xyz/jinhengtai/docs`

## SSL 证书管理
- 脚本 `deploy/scripts/renew_cert.sh` 使用 Certbot Webroot 模式续期 `jinhengtai.yidasoftware.xyz` 与 `api.jinhengtai.yidasoftware.xyz`
- 如需为 `yidasoftware.xyz` & `www.yidasoftware.xyz` 申请证书，请确保在脚本中新增域名参数或手动执行
- 证书续期后脚本会自动复制到 `deploy/certs/` 并执行 `systemctl reload nginx`

## Nginx 域名与路径配置说明
- 配置文件：`deploy/nginx/conf.d/api.conf`
- 已定义的 server 块：
  1. `default_server` 80 -> 直接转发到 `http://api:8000`，允许通过 IP 访问
  2. `jinhengtai.yidasoftware.xyz` 80 -> 强制跳转 HTTPS
  3. `yidasoftware.xyz` 80 -> 强制跳转 HTTPS
  4. `jinhengtai.yidasoftware.xyz` 443 -> 转发到 `http://api:8000`
  5. `yidasoftware.xyz` 443 -> 针对 `/jinhengtai/` 路径做重写并转发到 `http://api:8000`
- `/jinhengtai/` 路径规则：
  - 访问 `https://yidasoftware.xyz/jinhengtai/anything` => 实际转发为 `http://api:8000/anything`
  - `/jinhengtai`（无尾斜线）会自动 301 跳转到 `/jinhengtai/`
  - `/jinhengtai/` 之外的路径默认返回 404，避免误用主域名
- 更新配置后执行 `sudo docker compose up -d --build nginx` 或 `sudo docker compose restart nginx`

## 常用运维命令
```bash
# 拉取最新镜像并重启（在 /opt/jinhengtai-backend）
sudo docker compose pull
sudo docker compose up -d --build --remove-orphans

# 查看容器状态与日志
sudo docker compose ps
sudo docker compose logs -f nginx
sudo docker compose logs -f api

# 仅重载 Nginx（不重启容器）
sudo systemctl reload nginx

# 完整重启 Nginx 容器
sudo docker compose restart nginx
```

## 访问验证清单
1. `curl -I https://api.jinhengtai.yidasoftware.xyz/health` 返回 200/204
2. `curl -I https://yidasoftware.xyz/jinhengtai/health` 返回 200/204，且响应头 `location` 中无 `/jinhengtai/` 重复
3. `https://yidasoftware.xyz/jinhengtai/docs` 正常展示 Swagger UI
4. 小程序端调用可获取分类、商品列表、轮播图数据（参见 `miniprogram/services/*.js`）

## 常见问题排查
- **访问 404**：确认访问路径是否包含 `/jinhengtai/` 前缀，或确认 DNS 已指向服务器
- **证书无效**：检查 `/etc/letsencrypt/live/` 与 `deploy/certs/` 是否同步更新；必要时重新执行续期脚本
- **API 超时/错误**：使用 `sudo docker compose logs -f api` 查看 FastAPI 日志，确认数据库连通性
- **数据库无法连接**：确保 `mssql` 容器运行正常，并在 `.env` 中使用容器内网地址（例：`mssql`）

---

最近更新：新增 `https://yidasoftware.xyz/jinhengtai/` 域名转发支持与 Nginx 配置说明（2025-11-11）
