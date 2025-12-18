from fastapi import APIRouter,status,HTTPException,Depends
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(prefix='/users',tags=['Users'])

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {id} is not found')
    return user

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.User,db:Session=Depends(get_db)):
    hashed_passwod = utils.hashed(user.password)
    user.password = hashed_passwod
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user