from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 注册时接收的数据
class UserRegister(BaseModel):
    username: str = Field(..., min_length=4, max_length=32)
    password: str = Field(..., min_length=8)

# 登录时接收的数据
class UserLogin(BaseModel):
    username: str
    password: str

# 返回给前端的用户信息（不含密码）
class UserOut(BaseModel):
    id:         int
    username:   str
    nickname:   Optional[str]
    email:      Optional[str]
    avatar:     Optional[str]
    points:     int
    created_at: datetime

    class Config:
        from_attributes = True

# 登录成功返回的Token
class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserOut