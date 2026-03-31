# 🎬 MiniStream

基于 HLS 协议的全栈流媒体平台，支持视频上传、自动转码、在线播放。

![技术栈](https://img.shields.io/badge/前端-HTML%2FCSS%2FJS-blue)
![技术栈](https://img.shields.io/badge/后端-FastAPI-green)
![技术栈](https://img.shields.io/badge/数据库-MySQL%2BRedis-orange)
![技术栈](https://img.shields.io/badge/转码-FFmpeg%2BHLS-red)

## ✨ 功能特性

- 视频上传 → FFmpeg 自动转码 → HLS 切片
- 自适应流媒体播放（HLS.js）
- 用户注册 / 登录（JWT 认证）
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
│   └── profile.html   # 用户中心
├── backend/           # 后端
│   └── app/
│       ├── api/       # 接口路由
│       ├── models/    # 数据库模型
│       ├── schemas/   # 数据验证
│       ├── database.py
│       └── main.py
├── storage/           # 存储目录
│   ├── uploads/       # 原始视频
│   └── hls/           # HLS切片
└── worker/            # 转码队列（开发中）
```

## 🚀 本地运行

### 环境要求

- Python 3.11+
- Node.js 18+
- FFmpeg
- Docker Desktop
- Git

### 第一步：克隆项目
```bash
git clone https://github.com/Pope-zZZ/ministream.git
cd ministream
```

### 第二步：启动数据库
```bash
docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=ministream mysql:8.0
docker run -d --name redis -p 6379:6379 redis:latest
```

### 第三步：启动后端
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 第四步：启动前端
```bash
# 新开终端
python -m http.server 3000 --directory frontend
```

### 第五步：启动视频服务
```bash
# 新开终端
python backend/server.py
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:3000 |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| 视频服务 | http://localhost:8080 |

## 📝 API 文档

启动后端后访问 http://localhost:8000/docs 查看完整接口文档。

主要接口：

- `POST /api/auth/register` 注册
- `POST /api/auth/login` 登录
- `POST /api/videos/upload` 上传视频
- `GET /api/videos/` 获取视频列表
- `GET /api/videos/{id}` 获取视频详情

## 📌 开发进度

- [x] 前端页面（7个页面）
- [x] FastAPI 后端框架
- [x] 用户注册/登录（JWT）
- [x] 视频上传/转码/播放
- [ ] 异步转码队列（Celery）
- [ ] 前后端完整对接
- [ ] Docker Compose 一键部署

## 📄 License

MIT