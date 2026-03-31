from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.history import WatchHistory
# from app.models.video import Video
from app.schemas.history import HistoryUpdate, HistoryOut
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/history", tags=["播放记录"])


# ── 上报播放进度 ──
@router.post("/progress")
def update_progress(
    data: HistoryUpdate,
    db:   Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # video = db.query(Video).filter(Video.id == data.video_id).first()
    # if not video:
    #     raise HTTPException(status_code=404, detail="视频不存在")

    record = db.query(WatchHistory).filter(
        WatchHistory.user_id  == current_user.id,
        WatchHistory.video_id == data.video_id
    ).first()

    if record:
        record.progress = data.progress
        record.duration = data.duration
    else:
        record = WatchHistory(
            user_id  = current_user.id,
            video_id = data.video_id,
            progress = data.progress,
            duration = data.duration
        )
        db.add(record)

    db.commit()
    return {"message": "ok"}


# ── 获取某个视频的播放进度 ──
@router.get("/progress/{video_id}")
def get_progress(
    video_id: int,
    db:       Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(WatchHistory).filter(
        WatchHistory.user_id  == current_user.id,
        WatchHistory.video_id == video_id
    ).first()

    if not record:
        return {"progress": 0, "duration": 0}

    return {"progress": record.progress, "duration": record.duration}


# ── 获取用户全部播放历史（最近50条）──
@router.get("/", response_model=List[HistoryOut])
def get_history(
    db:   Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(WatchHistory).filter(
        WatchHistory.user_id == current_user.id
    ).order_by(WatchHistory.updated_at.desc()).limit(50).all()

    return [
    HistoryOut(
        video_id   = r.video_id,
        progress   = r.progress,
        duration   = r.duration,
        updated_at = r.updated_at,
        title      = None,   # 暂时不联表
        cover      = None,
        category   = None,
    )
    for r in records
]