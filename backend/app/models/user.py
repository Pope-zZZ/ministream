from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True, index=True)
    username    = Column(String(32), unique=True, index=True, nullable=False)
    nickname    = Column(String(32), nullable=True)
    password    = Column(String(128), nullable=False)
    email       = Column(String(64), nullable=True)
    avatar      = Column(String(256), nullable=True)
    points      = Column(Integer, default=10)        # 注册送10积分
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, server_default=func.now())
    last_login  = Column(DateTime, nullable=True)
    last_ip     = Column(String(45), nullable=True)