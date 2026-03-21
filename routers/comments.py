from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from security import access
from database import get_db
import models, schemas
from sqlalchemy import or_,func,DateTime
from typing import List


router = APIRouter(
    prefix="/posts/{post_id}",      
    tags=['Comments']        
)



@router.post("/comments",response_model=schemas.CommentOut)
def comment_post(
    post_id:int,
    new_comment:schemas.CommentCreate,
    db:Session=Depends(get_db),
    user:User=Depends(access)
):

    found_post=db.query(models.Post).filter(models.Post.id==post_id).first()

    if found_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )


    if not new_comment.content.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="comments cannot be empty" )

    comment=models.Comment(user_id=user.id,post_id=post_id,content=new_comment.content.strip(),is_deleted=False)

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@router.get("/comments",response_model=List[schemas.CommentOut])
def get_comments(
    post_id:int,
    db:Session=Depends(get_db)
):

    post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )

    all_comments=(
        db.query(models.Comment)
        .options(joinedload(models.Comment.user))
        .filter(models.Comment.post_id==post_id)
        .order_by(models.Comment.created_at.asc())
        .all()
        )

    return all_comments


@router.delete("/comments/{comment_id}",response_model=schemas.CommentOut)
def delete_comments(
    post_id:int,
    comment_id:int,
    db:Session=Depends(get_db),
    user:models.User=Depends(access)
):

    post=db.query(models.Post).filter(models.Post.id==post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )


    comment=db.query(models.Comment).filter(models.Comment.post_id==post_id,
            models.Comment.id==comment_id).first()

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not exist" )


    if comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you don't have permission" )

    if comment.is_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="comment already deleted" )

    comment.is_deleted=True
    
    db.commit()
    db.refresh(comment)

    return comment