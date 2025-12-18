from fastapi.security import OAuth2PasswordBearer
from .config import settings
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from . import database,models
from .schemas import TokenData
from jose import JWTError,jwt
from datetime import datetime,timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt
    
def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:int = payload.get("user_id")
        if user_id is None:
            raise credential_exception
        token_data = TokenData(id=user_id)
        return token_data
    except JWTError:
        raise credential_exception
    
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={'WWW-Authenticate':'Bearer'})

    token_data = verify_access_token(token,credential_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credential_exception
    return user