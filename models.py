from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    name= Column(String, unique=True)
    id = Column(Integer, primary_key=True)
    email= Column(String(120), unique=True)
    hash_password= Column(String)

    posts = relationship("Post",back_populates="owner")
    comments =relationship("Comment",back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    created_at =Column(DateTime,default=datetime.utcnow)
    updated_at =Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    owner_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship("User",back_populates="posts")

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    category=relationship("Category",back_populates="posts")

    ai_summary =Column(String,nullable=True)

class Category(Base):
    __tablename__ ="categories"
    id=Column(Integer,primary_key=True, index=True)
    name = Column(String)
    posts=relationship("Post",back_populates="category")


class Vote(Base):
    __tablename__ = "votes"
    user_id=Column(Integer,ForeignKey("users.id"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)

class Comment(Base):
    __tablename__ = "comments"
    id= Column(Integer,primary_key=True, index=True)
    user_id= Column(Integer,ForeignKey("users.id"))
    post_id= Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"))
    content= Column(String)
    created_at= Column(DateTime,default=datetime.utcnow)
    is_deleted= Column(Boolean,default=False)

    user=relationship("User",back_populates="comments")