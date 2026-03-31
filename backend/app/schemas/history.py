from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HistoryUpdate(BaseModel):
    video_id: int
    progress: float    # 当前播放秒数
    duration: float    # 视频总时长秒数

class HistoryOut(BaseModel):
    video_id:   int
    progress:   float
    duration:   float
    updated_at: datetime
    title:      Optional[str] = None
    cover:      Optional[str] = None
    category:   Optional[str] = None

    class Config:
        from_attributes = True