# 微信小程序电商系统部署指南

## 项目概述

已成功将微信小程序云开发项目迁移到云主机架构，包含：

✅ **已完成**
- MSSQL Server 2019 数据库设计和表结构
- Node.js + TypeScript + Express.js 后端API服务
- 完整的用户认证、商品管理、购物车、订单系统
- 文件上传和管理后台API
- 测试服务器验证

⏳ **待完成**
- 微信支付集成
- React管理后台
- Nginx配置和云主机部署
- 小程序API地址更新

## 部署架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   微信小程序    │────│   Node.js API   │────│  MSSQL Server   │
│   (前端)       │    │   (后端)       │    │   (数据库)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │  React管理后台   │
                       │  (管理界面)     │
                       └─────────────────┘
```

## 数据库信息

- **服务器**: 152.136.13.33,1433
- **用户名**: sa
- **密码**: YourStrong@Passw0rd
- **数据库名**: MiniAppEcommerce

## 后端API服务

### 技术栈
- Node.js 18+
- TypeScript
- Express.js
- Sequelize ORM
- JWT认证
- Multer文件上传

### 主要功能模块
1. **用户认证** (`/api/auth`)
   - 微信小程序登录
   - JWT令牌管理
   - 用户信息管理

2. **商品管理** (`/api/products`)
   - 商品列表、详情
   - 分类管理
   - 搜索功能
   - 库存管理

3. **购物车** (`/api/cart`)
   - 添加、删除商品
   - 数量更新
   - 选中状态管理

4. **订单系统** (`/api/orders`)
   - 订单创建
   - 状态管理
   - 订单查询

5. **支付系统** (`/api/payment`)
   - 微信支付集成
   - 支付回调
   - 退款处理

6. **管理后台** (`/api/admin`)
   - 管理员认证
   - 系统设置
   - 数据统计

### 启动方式

```bash
# 进入后端目录
cd backend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库连接等信息

# 开发模式启动
npm run dev

# 生产模式启动
npm run build
npm start
```

### 测试接口

使用提供的测试服务器：

```bash
# 启动测试服务器
node test-server.js
```

主要测试接口：
- 健康检查: `http://localhost:3001/health`
- API信息: `http://localhost:3001/api`
- 商品列表: `http://localhost:3001/api/products`
- 分类列表: `http://localhost:3001/api/categories`

## 数据库表结构

### 核心表

1. **Users** - 用户表
   - OpenId, UnionId
   - 用户基本信息
   - 状态管理

2. **Products** - 商品表
   - 商品基本信息
   - 价格、库存、销量
   - 状态管理

3. **Categories** - 分类表
   - 分类信息
   - 层级关系

4. **Cart** - 购物车表
   - 用户购物车数据
   - 商品数量、选中状态

5. **Orders** - 订单表
   - 订单基本信息
   - 收货信息
   - 状态管理

6. **OrderItems** - 订单明细表
   - 订单商品详情
   - 规格信息

7. **Admins** - 管理员表
   - 管理员账户
   - 权限管理

8. **Settings** - 系统配置表
   - 系统参数
   - 配置管理

详细表结构请参考 `backend/database/schema.sql`

## 下一步部署计划

### 1. 微信支付集成
- 配置微信支付参数
- 实现统一下单接口
- 处理支付回调
- 退款功能

### 2. React管理后台
- 创建React项目
- 使用Ant Design UI库
- 实现商品管理页面
- 实现订单管理页面
- 实现数据统计页面

### 3. 云主机部署
- 配置Nginx反向代理
- 部署Node.js服务
- 部署React管理后台
- 配置SSL证书
- 设置自动启动

### 4. 小程序更新
- 更新API基础URL
- 测试所有接口功能
- 确保支付流程正常
- 用户体验测试

## GitHub Actions CI/CD

建议的部署流程：

```yaml
name: Deploy to Cloud Server

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    - name: Install dependencies
      run: npm install
    - name: Run tests
      run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to server
      run: |
        # 部署脚本
        scp -r ./ user@server:/path/to/app
        ssh user@server "cd /path/to/app && npm install && npm run build && pm2 restart app"
```

## 环境变量配置

```env
# 服务器配置
NODE_ENV=production
PORT=3000
HOST=0.0.0.0

# 数据库配置
DB_HOST=152.136.13.33
DB_PORT=1433
DB_NAME=MiniAppEcommerce
DB_USER=sa
DB_PASSWORD=YourStrong@Passw0rd

# JWT配置
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=7d

# 微信小程序配置
WECHAT_APP_ID=your-wechat-app-id
WECHAT_APP_SECRET=your-wechat-app-secret

# 微信支付配置
WECHAT_MCH_ID=your-merchant-id
WECHAT_API_KEY=your-api-key
```

## 监控和维护

### 日志管理
- 使用PM2管理进程
- 配置日志轮转
- 监控错误日志

### 备份策略
- 数据库定期备份
- 文件系统备份
- 配置文件备份

### 性能优化
- 数据库索引优化
- API响应缓存
- 图片CDN加速

## 安全考虑

1. **API安全**
   - JWT令牌验证
   - 请求频率限制
   - 输入数据验证

2. **数据库安全**
   - 连接加密
   - 定期更新密码
   - 最小权限原则

3. **文件上传安全**
   - 文件类型验证
   - 大小限制
   - 病毒扫描

## 联系支持

如果在部署过程中遇到问题，请参考：
1. 项目README文件
2. API文档
3. 数据库schema文件
4. 错误日志

---

**部署状态**: ✅ 后端API完成 | ⏳ 管理后台开发中 | ⏳ 支付集成待完成