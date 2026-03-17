
from passlib.context import CryptContext
from jose import jwt,JWTError, ExpiredSignatureError
from models import User
from fastapi import HTTPException,Depends
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


# 这里的逻辑是：创建一个使用 bcrypt 算法的“粉碎机”环境
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")#OAuth2PasswordBearer是生成一个感应门的图纸

def access(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    
    try:
    # 尝试拆盲盒
        decode = jwt.decode(token, 'secret', algorithms=['HS256'])
        name=decode.get('sub')

        if not name:
            raise HTTPException(status_code=401, detail="not login" )
    
    
    except ExpiredSignatureError:
    # 如果法医鉴定为：手环已过期！
        raise HTTPException(status_code=401, detail="not login" )
    
    except JWTError:
    # 如果法医鉴定为：这根本不是我们发的手环（瞎编的、篡改的）！
        raise HTTPException(status_code=401, detail="not login" )

    user=db.query(User).filter(name==User.name).first()

    if not user:
        raise HTTPException(status_code=401, detail="not login" )

    return user