from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from security import access

router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/")
def post_vote(
    to_vote:schemas.VoteCreate,
    db:Session=Depends(get_db),
    user:User=Depends(access)
):
    db_post=db.query(models.Post).filter(to_vote.post_id==models.Post.id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist" )

    vote_post=db.query(models.Vote).filter(
        to_vote.post_id==models.Vote.post_id,
        user.id==models.Vote.user_id
    ).first()

    dir=to_vote.dir

    if dir==1:
        if vote_post is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="cannot like twice" )

        else:
            vote_post=models.Vote(post_id=to_vote.post_id,user_id=user.id)
            db.add(vote_post)
            db.commit()
            return {"message":"like successful!", "post_id":vote_post.post_id}

    else:
        if vote_post is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="you haven't like" )

        else:
            db.delete(vote_post)
            db.commit()
            return {"message":"unlike successful!", "post_id":to_vote.post_id}