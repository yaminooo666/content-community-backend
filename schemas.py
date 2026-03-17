from pydantic import BaseModel,ConfigDict
from typing import Optional,Literal


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
    
    owner:UserOut
    category:Optional[CategoryOut]=None

    model_config = ConfigDict(from_attributes=True)


class PostOutWithVotes(BaseModel):
    Post:PostOut
    votes:int

    model_config = ConfigDict(from_attributes=True)


class UpdatePost(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
    category_id:Optional[int]=None

class VoteCreate(BaseModel):
    dir:Literal[0,1]
    post_id:int

