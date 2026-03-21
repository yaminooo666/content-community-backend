
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from security import access
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import models, schemas
from sqlalchemy import or_,func,DateTime
from datetime import datetime
from google import genai
from config import settings


client = genai.Client(api_key=settings.gemini_api_key)


router = APIRouter(
    prefix="/posts",      
    tags=['Posts']        
)


def generate_summary(title:str,content:str) ->str:
    prompt = f"""请根据给定的标题和正文，生成一段 80 字以内的中文摘要。摘要必须简洁、准确，只概括原文已有信息，不要编造、扩展或加入评价。只返回摘要正文，不要加前缀或说明。

        标题：{title}
        正文：{content}
        """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        return f"{title} {content}".strip()[:80]


@router.post("/",response_model=schemas.PostOut)
def post_page(
    post_context:schemas.CreatePost,
    current_user:models.User=Depends(access),
    db:Session=Depends(get_db)):

    owner_id=current_user.id

    current_post=models.Post(owner_id=owner_id,
                title=post_context.title,
                content=post_context.content,
                category_id=post_context.category_id
                )


    db.add(current_post)
    db.commit()
    db.refresh(current_post)

    current_post.ai_summary=generate_summary(current_post.title,current_post.content)

    db.commit()
    db.refresh(current_post)

    return current_post


@router.post("/categories",response_model=schemas.CategoryOut)
def create_category(name:str,db:Session=Depends(get_db)):
    new_category=models.Category(name=name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/me",response_model=List[schemas.PostOut])
def get_my_posts(current_user: models.User = Depends(access)):
   
    return current_user.posts



@router.get("/{post_id}",response_model=schemas.PostOutWithVotes)
def get_post(
    post_id:int,
    db:Session=Depends(get_db)
):
    current_post=(
        db.query(models.Post,func.count(models.Vote.post_id).label("votes"))
        .outerjoin(models.Vote,models.Post.id==models.Vote.post_id)
        .options(joinedload(models.Post.category))
        .filter(models.Post.id==post_id)
        .group_by(models.Post.id)
        .first())

    if current_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )

    return {"post":current_post[0],"votes":current_post[1]}



@router.delete("/{post_id}")
def delete_post(
    post_id:int,
    db:Session=Depends(get_db),
    current_user:models.User=Depends(access)
):
    post_to_delete=db.query(models.Post).filter(models.Post.id==post_id).first()

    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )

    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you don't have permission" )

    db.delete(post_to_delete)
    db.commit()

    return {"message": f"ID为 {post_id} 的日记已成功清理门户！"}


@router.patch("/{post_id}",response_model=schemas.PostOut)
def update_post(
    update_data:schemas.UpdatePost,
    post_id:int,
    db:Session=Depends(get_db),
    current_user:models.User=Depends(access)
):
    post_to_update=db.query(models.Post).filter(post_id==models.Post.id).first()

    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )

    if current_user.id != post_to_update.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you don't have permission" )

    if update_data.title is not None:
        if update_data.title.strip():
            post_to_update.title=update_data.title.strip()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title cannot be empty" )

    if update_data.content is not None:
        if update_data.content.strip():
            post_to_update.content=update_data.content.strip()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cotent cannot be empty" )

    if update_data.category_id is not None:
        post_to_update.category_id=update_data.category_id

    post_to_update.ai_summary = generate_summary(post_to_update.title, post_to_update.content)

    db.commit()
    db.refresh(post_to_update)

    return post_to_update




@router.get("/",response_model=schemas.PostListOut)
def get_posts(
    db:Session=Depends(get_db),
    limit:int=10,skip:int=0,
    search:str="",
    author: str = ""):

    search = search.strip()
    author = author.strip()

    if limit<=0 or limit>50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="limit must be between 1 and 50" )

    if skip<0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="skip cannot be negative" )

    query=db.query(models.Post,func.count(models.Vote.post_id).label("votes")
        ).select_from(models.Post
        ).options(joinedload(models.Post.category)
        ).join(models.User
        ).outerjoin(models.Vote, models.Vote.post_id == models.Post.id
        ).group_by(models.Post.id)

    if search:
        query=query.filter(or_(models.Post.title.icontains(search),models.Post.content.icontains(search)))

    if author:
        query=query.filter(models.User.name.icontains(author))

    all_post=query.order_by(models.Post.id.desc()).limit(limit).offset(skip).all()

    items=[{"post": row[0], "votes": row[1] } for row in all_post]


    total_query=db.query(models.Post).join(models.User)
    if search:
        total_query=total_query.filter(or_(models.Post.title.icontains(search),models.Post.content.icontains(search)))

    if author:
        total_query=total_query.filter(models.User.name.icontains(author))

    total=total_query.count()

    return {
        "items":items,
        "limit":limit,
        "skip":skip,
        "total":total
    }


