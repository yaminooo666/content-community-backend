
import models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from security import access,get_password_hash, verify_password
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt


router = APIRouter(  
    prefix="/auth",
    tags=['Auth']        
)


@router.post("/register")
def register(user_in:schemas.CreateUser,db:Session=Depends(get_db)):
   
    exist_name=db.query(models.User).filter(models.User.name == user_in.name).first()
    if exist_name is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already taken" )

    exist_email=db.query(models.User).filter(models.User.email == user_in.email).first()
    if exist_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already taken" )

    password=user_in.password
    hashed_password=get_password_hash(password)

    user=models.User(name=user_in.name,email=user_in.email,hash_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message":f"success regist {user_in.name}"}

@router.post("/login")
def login(user_in: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):

    db_user=db.query(models.User).filter(models.User.name==user_in.username).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not exist" )


    if not verify_password(user_in.password, db_user.hash_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not exist" )

    access_token= jwt.encode({'sub': db_user.name}, 'secret', algorithm='HS256')

    return {"access_token":access_token, "token_type": "bearer"}

@router.get("/user/me")
def user_page(current_user:models.User=Depends(access)):
   
    return {
        "message": f"尊贵的 VIP {current_user.name}，欢迎进入机密档案室！",
        "你的加密密码长这样": current_user.hash_password}
        


