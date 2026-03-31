# 🎬 MiniStream

基于 HLS 协议的全栈流媒体平台，支持视频上传、自动转码、在线播放。

![](https://img.shields.io/badge/前端-HTML%2FCSS%2FJS-blue)
![](https://img.shields.io/badge/后端-FastAPI-green)
![](https://img.shields.io/badge/数据库-MySQL%2BRedis-orange)
![](https://img.shields.io/badge/转码-FFmpeg%2BHLS-red)

## ✨ 功能特性

- 视频上传 → FFmpeg 自动转码 → HLS 切片
- 自适应流媒体播放（HLS.js）
- 用户注册 / 登录（JWT + bcrypt 认证）
- 番剧列表、筛选、分页
- 播放页（线路切换、选集、相关推荐）
- 用户中心（播放记录、收藏、消息通知）

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML / CSS / JavaScript / HLS.js |
| 后端 | Python / FastAPI / SQLAlchemy |
| 数据库 | MySQL 8.0 / Redis |
| 转码 | FFmpeg / HLS |
| 部署 | Docker / Nginx |

## 📁 项目结构
```
ministream/
├── frontend/          # 前端页面
│   ├── index.html     # 首页
│   ├── show-anime.html # 日番列表
│   ├── show-movie.html # 剧场版列表
│   ├── player.html    # 播放页
│   ├── login.html     # 登录
│   ├── register.html  # 注册
│   ├── profile.html   # 用户中心
│   └── api.js         # 前端API工具
├── backend/
│   ├── app/
│   │   ├── api/       # 接口路由（auth/videos）
│   │   ├── models/    # 数据库模型
│   │   ├── schemas/   # 数据验证
│   │   ├── database.py
│   │   └── main.py    # 入口文件
│   ├── Dockerfile
│   └── requirements.txt
├── nginx/
│   └── nginx.conf     # 反向代理配置
├── storage/
│   ├── uploads/       # 原始视频（不上传Git）
│   └── hls/           # HLS切片文件
├── docker-compose.yml
└── README.md
```

## 🚀 本地运行

### 环境要求

| 工具 | 说明 |
|------|------|
| Python 3.11+ | 安装时勾选 Add to PATH |
| FFmpeg | 解压后配置环境变量 |
| Docker Desktop | 安装后重启电脑 |
| Git | 用于拉取代码 |

### 第一步：克隆项目
```bash
git clone https://github.com/Pope-zZZ/ministream.git
cd ministream
```

### 第二步：启动数据库
```bash
docker run -d --name mysql -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=ministream \
  mysql:8.0

docker run -d --name redis -p 6379:6379 redis:latest
```

### 第三步：安装后端依赖
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 第四步：启动后端
```bash
uvicorn app.main:app --reload --port 8000
```

### 第五步：启动前端页面服务
```bash
# 新开终端，在项目根目录
python -m http.server 3000 --directory frontend
```

### 第六步：启动视频文件服务
```bash
# 再新开一个终端
python backend/server.py
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:3000 |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| 视频服务 | http://localhost:8080 |

## 🐳 Docker 一键启动（推荐）
```bash
docker-compose up -d
```

访问 http://localhost 即可，无需手动启动各个服务。

## 📝 API 文档

启动后端后访问 http://localhost:8000/docs 查看完整接口文档。

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/auth/register | POST | 注册 |
| /api/auth/login | POST | 登录 |
| /api/auth/me | GET | 获取当前用户 |
| /api/videos/upload | POST | 上传视频 |
| /api/videos/ | GET | 获取视频列表 |
| /api/videos/{id} | GET | 获取视频详情 |
| /api/videos/{id} | DELETE | 删除视频 |

## ❓ 常见问题

**Q：启动后端报数据库连接错误？**
```bash
docker ps          # 检查容器是否运行
docker start mysql # 重新启动
```

**Q：视频播放没有画面？**
- 确认 `python backend/server.py` 正在运行
- 确认 `storage/hls/` 目录下有 `.m3u8` 文件

**Q：登录后刷新变回未登录？**
- 检查浏览器是否禁用了 localStorage

## 📌 开发进度

- [x] 前端页面（7个页面）
- [x] FastAPI 后端框架
- [x] 用户注册/登录（JWT + bcrypt）
- [x] 视频上传/转码/HLS切片
- [x] 前后端真实对接
- [x] Docker Compose 一键部署
- [ ] 异步转码队列（Celery）
- [x] 弹幕系统（WebSocket）

## 📄 License

MIT