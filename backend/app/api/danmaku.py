from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
import json

from app.database import get_db
from app.models.danmaku import Danmaku
from app.schemas.danmaku import DanmakuOut

router = APIRouter(prefix="/danmaku", tags=["弹幕"])

# ── 连接管理器 ──
class ConnectionManager:
    def __init__(self):
        # {video_id: [ws1, ws2, ...]}
        self.rooms: Dict[int, List[WebSocket]] = {}

    async def connect(self, video_id: int, ws: WebSocket):
        await ws.accept()
        if video_id not in self.rooms:
            self.rooms[video_id] = []
        self.rooms[video_id].append(ws)
        print(f"[弹幕] 用户加入房间 video_{video_id}，当前人数：{len(self.rooms[video_id])}")

    def disconnect(self, video_id: int, ws: WebSocket):
        if video_id in self.rooms:
            self.rooms[video_id].remove(ws)
            print(f"[弹幕] 用户离开房间 video_{video_id}，当前人数：{len(self.rooms[video_id])}")

    async def broadcast(self, video_id: int, message: dict, sender: WebSocket = None):
        """广播给同一视频的所有用户"""
        if video_id not in self.rooms:
            return
        dead = []
        for ws in self.rooms[video_id]:
            if ws == sender:
                continue  # 不发给自己
            try:
                await ws.send_json(message)
            except:
                dead.append(ws)
        for ws in dead:
            self.rooms[video_id].remove(ws)

manager = ConnectionManager()

# ── WebSocket 弹幕接口 ──
@router.websocket("/ws/{video_id}")
async def danmaku_ws(
    video_id: int,
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    await manager.connect(video_id, websocket)

    # 发送历史弹幕（最近200条）
    history = db.query(Danmaku)\
        .filter(Danmaku.video_id == video_id)\
        .order_by(Danmaku.time_point)\
        .limit(200).all()

    await websocket.send_json({
        "type": "history",
        "data": [
            {
                "id": d.id,
                "content": d.content,
                "time_point": d.time_point,
                "color": d.color,
                "type": d.type,
                "username": "匿名"
            } for d in history
        ]
    })

    try:
        while True:
            # 接收用户发送的弹幕
            raw = await websocket.receive_text()
            data = json.loads(raw)

            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                continue

            if data.get("type") == "danmaku":
                content    = data.get("content", "").strip()
                time_point = float(data.get("time_point", 0))
                color      = data.get("color", "#ffffff")
                dm_type    = int(data.get("dm_type", 0))
                username   = data.get("username", "匿名")

                if not content or len(content) > 100:
                    continue

                # 存数据库
                danmaku = Danmaku(
                    video_id=video_id,
                    content=content,
                    time_point=time_point,
                    color=color,
                    type=dm_type
                )
                db.add(danmaku)
                db.commit()
                db.refresh(danmaku)

                # 广播给其他用户
                msg = {
                    "type": "danmaku",
                    "id": danmaku.id,
                    "content": content,
                    "time_point": time_point,
                    "color": color,
                    "dm_type": dm_type,
                    "username": username
                }
                await manager.broadcast(video_id, msg, sender=websocket)
                # 也发给自己确认
                await websocket.send_json({**msg, "self": True})

    except WebSocketDisconnect:
        manager.disconnect(video_id, websocket)

# ── REST 接口：获取弹幕列表 ──
@router.get("/{video_id}", response_model=List[DanmakuOut])
def get_danmaku(video_id: int, db: Session = Depends(get_db)):
    return db.query(Danmaku)\
        .filter(Danmaku.video_id == video_id)\
        .order_by(Danmaku.time_point)\
        .all()