
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from security import access
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import models, schemas
from sqlalchemy import or_,func


router = APIRouter(
    prefix="/posts",      
    tags=['Posts']        
)


@router.post("/")
def post_page(
    post_context:schemas.CreatePost,
    current_user:models.User=Depends(access),
    db:Session=Depends(get_db)):

    owner_id=current_user.id

    current_post=models.Post(owner_id=owner_id,title=post_context.title,content=post_context.content,category_id=post_context.category_id)
    db.add(current_post)
    db.commit()
    db.refresh(current_post)

    return {"message": "发布成功！", "post_id": current_post.id}


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
    update_date:schemas.UpdatePost,
    post_id:int,
    db:Session=Depends(get_db),
    current_user:models.User=Depends(access)
):
    post_to_update=db.query(models.Post).filter(post_id==models.Post.id).first()

    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )

    if current_user.id != post_to_update.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you don't have permission" )

    if update_date.title is not None:
        post_to_update.title=update_date.title

    if update_date.content is not None:
        post_to_update.content=update_date.content

    if update_date.category_id is not None:
        post_to_update.category_id=update_date.category_id

    db.commit()
    db.refresh(post_to_update)

    return post_to_update


@router.get("/",response_model=List[schemas.PostOutWithVotes])
def get_posts(
    db:Session=Depends(get_db),
    limit:int=10,skip:int=0,
    search:str="",
    author: str = ""):

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

    return all_post


