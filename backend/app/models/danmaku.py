from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Danmaku(Base):
    __tablename__ = "danmaku"

    id         = Column(Integer, primary_key=True, index=True)
    video_id   = Column(Integer, ForeignKey("videos.id"), nullable=False, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=True)
    content    = Column(String(100), nullable=False)   # 弹幕内容
    time_point = Column(Float, nullable=False)          # 视频第几秒出现
    color      = Column(String(7), default="#ffffff")   # 弹幕颜色
    type       = Column(Integer, default=0)             # 0滚动 1顶部 2底部
    created_at = Column(DateTime, server_default=func.now())