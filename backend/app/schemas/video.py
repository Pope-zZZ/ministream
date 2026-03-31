from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.video import VideoStatus

# 上传视频时接收的数据
class VideoCreate(BaseModel):
    title:       str
    description: Optional[str] = None
    category:    Optional[str] = "日番"
    genre:       Optional[str] = None
    year:        Optional[int] = None
    rating:      Optional[str] = None

# 返回给前端的视频信息
class VideoOut(BaseModel):
    id:          int
    title:       str
    description: Optional[str]
    cover:       Optional[str]
    category:    Optional[str]
    genre:       Optional[str]
    year:        Optional[int]
    rating:      Optional[str]
    status:      VideoStatus
    hls_path:    Optional[str]
    duration:    Optional[int]
    views:       int
    created_at:  datetime

    class Config:
        from_attributes = True