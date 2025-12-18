from fastapi import Depends,status,APIRouter,HTTPException,Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from ..schemas import Task,TaskResponse,TaskOut,SingleTask
from typing import List,Optional
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)

@router.get('/',response_model=List[TaskResponse],status_code=status.HTTP_200_OK)
def get_tasks(db:Session=Depends(get_db),current:models.User=Depends(get_current_user),limit:int=10,skip:int=0,search:Optional[str]="",completed:Optional[bool]=False):
    query = db.query(models.Tasks).filter(models.Tasks.title.contains(search))
    query = query.filter(models.Tasks.completed == completed)
    return query.limit(limit).offset(skip).all()

@router.get('/mytasks',status_code=status.HTTP_200_OK,response_model=List[SingleTask])
def get_my_tasks(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).all()
    return tasks


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=SingleTask)
def create_task(task:Task,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    task = models.Tasks(owner_id=current_user.id,**task.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=TaskResponse)
def get_task(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'task with {id} is not found')
    return task

@router.put('/{id}',status_code=status.HTTP_200_OK,response_model=SingleTask)
def update_task(id:int,task:Task,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_task = db.query(models.Tasks).filter(models.Tasks.id == id)
    existing = db_task.first()
    if existing.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not allowed to perform this operation')
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'task with {id} is not found')
    db_task.update(task.dict(),synchronize_session=False)
    db.commit()
    updated = db_task.first()
    return updated

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not allowed to perform this operation')
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'task with id {id} is not found')
    db.delete(db_task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)