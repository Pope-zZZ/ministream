from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app.api import auth, videos, danmaku

# 导入所有模型，确保建表
from app.models import user, video, danmaku as danmaku_model

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MiniStream API",
    description="基于HLS协议的流媒体平台后端",
    version="1.0.0"
)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router,    prefix="/api")
app.include_router(videos.router,  prefix="/api")
app.include_router(danmaku.router, prefix="/api")

# 静态文件服务
app.mount(
    "/storage",
    StaticFiles(directory="D:/ministream/storage"),
    name="storage"
)

@app.get("/")
def root():
    return {"message": "MiniStream API 运行中 🎬"}

@app.get("/health")
def health():
    return {"status": "ok"}