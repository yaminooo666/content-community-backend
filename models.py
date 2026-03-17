from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    name= Column(String, unique=True)
    id = Column(Integer, primary_key=True)
    email= Column(String(120), unique=True)
    hash_password= Column(String)
    posts = relationship("Post",back_populates="owner")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)

    owner_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship("User",back_populates="posts")

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    category=relationship("Category",back_populates="posts")

class Category(Base):
    __tablename__ ="categories"
    id=Column(Integer,primary_key=True, index=True)
    name = Column(String)
    posts=relationship("Post",back_populates="category")


class Vote(Base):
    __tablename__ = "votes"
    user_id=Column(Integer,ForeignKey("users.id"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)