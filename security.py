
from passlib.context import CryptContext
from jose import jwt,JWTError, ExpiredSignatureError
from models import User
from fastapi import HTTPException,Depends
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import settings
from datetime import datetime, timedelta, timezone



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def access(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    
    try:
    
        decode = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"require_exp": True}
        )
        name=decode.get('sub')

        if not name:
            raise HTTPException(status_code=401, detail="not login" )
    
    
    except ExpiredSignatureError:
    
        raise HTTPException(status_code=401, detail="not login" )
    
    except JWTError:
    
        raise HTTPException(status_code=401, detail="not login" )

    user=db.query(User).filter(name==User.name).first()

    if not user:
        raise HTTPException(status_code=401, detail="not login" )

    return user

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )