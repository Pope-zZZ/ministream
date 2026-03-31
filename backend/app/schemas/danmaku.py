from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 发送弹幕
class DanmakuCreate(BaseModel):
    video_id:   int
    content:    str = Field(..., min_length=1, max_length=100)
    time_point: float
    color:      str = "#ffffff"
    type:       int = 0

# 返回弹幕
class DanmakuOut(BaseModel):
    id:         int
    video_id:   int
    user_id:    Optional[int]
    content:    str
    time_point: float
    color:      str
    type:       int
    created_at: datetime

    class Config:
        from_attributes = True

# WebSocket 消息格式
class DanmakuMessage(BaseModel):
    type:       str        # "danmaku" / "ping" / "history"
    video_id:   Optional[int] = None
    content:    Optional[str] = None
    time_point: Optional[float] = None
    color:      str = "#ffffff"
    username:   Optional[str] = "匿名"