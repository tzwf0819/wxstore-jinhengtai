# GitHub Secrets 配置指南

在GitHub仓库的Settings > Secrets and variables > Actions中的**JINHENGTAI**配置中添加以下Secrets：

## 🔐 JINHENGTAI配置中的Secrets

### 服务器连接
```
JINHENGTAI_HOST=152.136.13.33
JINHENGTAI_USERNAME=your_ssh_username
JINHENGTAI_PASSWORD=your_ssh_password
```

### 数据库配置
```
JINHENGTAI_DB_HOST=152.136.13.33
JINHENGTAI_DB_PORT=1433
JINHENGTAI_DB_NAME=MiniAppEcommerce
JINHENGTAI_DB_USER=sa
JINHENGTAI_DB_PASSWORD=YourStrong@Passw0rd
JINHENGTAI_INIT_DB=false  # 设置为true来初始化数据库
```

### JWT配置
```
JINHENGTAI_JWT_SECRET=your_super_secret_jwt_key_at_least_32_characters_long
```

### 微信小程序配置
```
JINHENGTAI_WECHAT_APP_ID=your_wechat_mini_program_app_id
JINHENGTAI_WECHAT_APP_SECRET=your_wechat_mini_program_app_secret
```

### 微信支付配置
```
JINHENGTAI_WECHAT_MCH_ID=your_merchant_id
JINHENGTAI_WECHAT_API_KEY=your_wechat_pay_api_key
JINHENGTAI_WECHAT_CERT_PATH=/opt/cloudbase/certs/apiclient_cert.pem
JINHENGTAI_WECHAT_KEY_PATH=/opt/cloudbase/certs/apiclient_key.pem
```

### 应用配置
```
JINHENGTAI_CORS_ORIGIN=https://yourdomain.com
JINHENGTAI_NODE_ENV=production
```

## 🚀 部署步骤

### 1. 首次部署
1. 在JINHENGTAI配置中添加所有必需的Secrets
2. 推送代码到main分支
3. 手动触发Database Setup workflow（设置init_database=true）
4. 手动触发Nginx Setup workflow
5. 等待Backend Deployment workflow自动完成

### 2. 后续部署
- 推送代码到main分支将自动触发Backend Deployment
- 可手动触发任何workflow

### 3. 监控
- Health Check workflow每5分钟自动运行
- 可在Actions页面查看部署状态

## 📋 验证部署

部署完成后，访问以下地址验证：

- **API健康检查**: http://152.136.13.33/health
- **API根路径**: http://152.136.13.33/api/
- **数据库状态**: http://152.136.13.33/api/health/db

## 🔧 故障排除

### 常见问题

1. **连接超时**
   - 检查JINHENGTAI_HOST和JINHENGTAI_USERNAME、JINHENGTAI_PASSWORD是否正确
   - 确认SSH用户名和密码正确

2. **数据库连接失败**
   - 验证JINHENGTAI_DB_HOST和JINHENGTAI_DB_PORT
   - 检查JINHENGTAI_DB_USER和JINHENGTAI_DB_PASSWORD

3. **服务启动失败**
   - 查看Actions日志
   - 检查环境变量配置

### 日志位置
- 应用日志: `/opt/cloudbase/logs/`
- PM2日志: `pm2 logs cloudbase-api`
- 系统日志: `/var/log/syslog`

## 🛠️ 手动操作

如需手动操作，可通过SSH连接到服务器：

```bash
ssh username@152.136.13.33

# 查看服务状态
pm2 status
pm2 logs cloudbase-api

# 重启服务
pm2 restart cloudbase-api

# 停止服务
pm2 stop cloudbase-api
```

## 📝 注意事项

- 所有Secrets都以`JINHENGTAI_`前缀命名
- 确保Secrets值不包含特殊字符或换行符
- 敏感信息（如密码、密钥）请妥善保管
- 定期更新密钥和密码以确保安全