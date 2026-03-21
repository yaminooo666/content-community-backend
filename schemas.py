from pydantic import BaseModel,ConfigDict
from typing import Optional,Literal,List
from datetime import datetime


class CreateUser(BaseModel):
    name:str
    email:str
    password:str

class LoginUser(BaseModel):
    name:str
    password:str

class CreatePost(BaseModel):
    title:str
    content:str
    category_id:Optional[int]=None

class UserOut(BaseModel):
    id: int
    name: str
    # 别忘了这个“翻译开关”，让它能读懂 SQLAlchemy 对象
    model_config = ConfigDict(from_attributes=True)


class CategoryOut(BaseModel):
    id:int
    name:Optional[str]=None

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    id:int
    title:str
    content:str

    created_at:datetime
    updated_at:datetime
    
    owner:UserOut
    category:Optional[CategoryOut]=None

    ai_summary:Optional[str]=None

    model_config = ConfigDict(from_attributes=True)


class PostOutWithVotes(BaseModel):
    post:PostOut
    votes:int

    model_config = ConfigDict(from_attributes=True)


class PostListOut(BaseModel):
    items: List[PostOutWithVotes]
    total: int
    limit: int
    skip: int


class UpdatePost(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
    category_id:Optional[int]=None
    

class VoteCreate(BaseModel):
    dir:Literal[0,1]
    post_id:int


class CommentCreate(BaseModel):
    content:str

class CommentOut(BaseModel):
    id:int
    created_at:datetime
    content:str
    is_deleted:bool
    user:UserOut

    model_config = ConfigDict(from_attributes=True)

