from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接地址
# 格式：mysql+pymysql://用户名:密码@地址:端口/数据库名
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ministream"

engine = create_engine(
    DATABASE_URL,
    echo=True,          # 打印SQL语句，开发阶段方便调试
    pool_pre_ping=True  # 自动检测连接是否有效
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 所有模型的基类
Base = declarative_base()

# 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()