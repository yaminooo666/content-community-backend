from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 1. 定义数据库地址（这里就在本地创建一个 test.db 文件）
SQLALCHEMY_DATABASE_URL = settings.database_url

# 2. 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3. 创建 Session 类（以后我们操作数据库的“手”）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建母类（Base），所有的数据库模型都会继承它
Base = declarative_base()

def get_db():
    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()