from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os, shutil, subprocess, uuid

from app.database import get_db
from app.models.video import Video, VideoStatus
from app.schemas.video import VideoCreate, VideoOut

router = APIRouter(prefix="/videos", tags=["视频"])

UPLOAD_DIR = "D:/ministream/storage/uploads"
HLS_DIR    = "D:/ministream/storage/hls"

def convert_to_hls(input_path: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    output_m3u8 = os.path.join(output_dir, "index.m3u8")
    cmd = [
        "ffmpeg", "-i", input_path,
        "-codec", "copy",
        "-start_number", "0",
        "-hls_time", "6",
        "-hls_list_size", "0",
        "-f", "hls",
        output_m3u8
    ]
    subprocess.run(cmd, check=True)
    return output_m3u8

# ── 上传视频 ──
@router.post("/upload", response_model=VideoOut)
async def upload_video(
    title:       str = Form(...),
    description: Optional[str] = Form(None),
    category:    str = Form("日番"),
    genre:       Optional[str] = Form(None),
    year:        Optional[int] = Form(None),
    rating:      Optional[str] = Form(None),
    file:        UploadFile = File(...),
    db:          Session = Depends(get_db)
):
    video_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    upload_path = os.path.join(UPLOAD_DIR, f"{video_id}{ext}")
    with open(upload_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    video = Video(
        title=title,
        description=description,
        category=category,
        genre=genre,
        year=year,
        rating=rating,
        original_path=upload_path,
        status=VideoStatus.processing
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    try:
        hls_output_dir = os.path.join(HLS_DIR, str(video.id))
        m3u8_path = convert_to_hls(upload_path, hls_output_dir)
        video.hls_path = m3u8_path
        video.status = VideoStatus.ready
    except Exception as e:
        video.status = VideoStatus.error
    finally:
        db.commit()

    db.refresh(video)
    return video

# ── 获取视频列表 ──
@router.get("/", response_model=List[VideoOut])
def get_videos(
    category: Optional[str] = None,
    genre:    Optional[str] = None,
    keyword:  Optional[str] = None,
    page:     int = 1,
    limit:    int = 24,
    db:       Session = Depends(get_db)
):
    query = db.query(Video).filter(Video.status == VideoStatus.ready)

    if category:
        query = query.filter(Video.category == category)
    if genre:
        query = query.filter(Video.genre == genre)
    if keyword:
        query = query.filter(Video.title.contains(keyword))

    videos = query.order_by(Video.created_at.desc())\
                  .offset((page - 1) * limit)\
                  .limit(limit).all()
    return videos

# ── 获取单个视频 ──
@router.get("/{video_id}", response_model=VideoOut)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    video.views += 1
    db.commit()
    db.refresh(video)
    return video

# ── 删除视频 ──
@router.delete("/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    if video.original_path and os.path.exists(video.original_path):
        os.remove(video.original_path)
    hls_dir = os.path.join(HLS_DIR, str(video_id))
    if os.path.exists(hls_dir):
        shutil.rmtree(hls_dir)

    db.delete(video)
    db.commit()
    return {"message": "删除成功"}