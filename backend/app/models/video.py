from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class VideoStatus(str, enum.Enum):
    pending    = "pending"     # 等待转码
    processing = "processing"  # 转码中
    ready      = "ready"       # 可以播放
    error      = "error"       # 转码失败

class Video(Base):
    __tablename__ = "videos"

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(String(128), nullable=False)       # 番剧标题
    description  = Column(Text, nullable=True)               # 简介
    cover        = Column(String(256), nullable=True)        # 封面图路径
    category     = Column(String(32), nullable=True)         # 分类：日番/剧场版
    genre        = Column(String(64), nullable=True)         # 类型：动作/奇幻...
    year         = Column(Integer, nullable=True)            # 年份
    rating       = Column(String(16), nullable=True)         # 评级：PG-12/R-15
    status       = Column(Enum(VideoStatus), default=VideoStatus.pending)
    hls_path     = Column(String(256), nullable=True)        # m3u8文件路径
    original_path = Column(String(256), nullable=True)       # 原始文件路径
    duration     = Column(Integer, nullable=True)            # 时长（秒）
    views        = Column(Integer, default=0)                # 播放次数
    uploader_id  = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at   = Column(DateTime, server_default=func.now())
    updated_at   = Column(DateTime, onupdate=func.now())

    uploader = relationship("User", backref="videos")