from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class WatchHistory(Base):
    __tablename__ = "watch_history"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id   = Column(Integer, nullable=False)    # 去掉外键
    progress   = Column(Float, default=0)
    duration   = Column(Float, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="watch_history")
    # video relationship 删掉

    __table_args__ = (
        UniqueConstraint("user_id", "video_id", name="uq_user_video"),
    )