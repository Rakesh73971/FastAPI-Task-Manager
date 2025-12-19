from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime,date
from .enum import PriorityEnum


class Task(BaseModel):
    title : str
    description : str
    completed : bool = False
    due_date : date
    priority : PriorityEnum


class SingleTask(BaseModel):
    id : int
    title : str
    description : str
    completed : bool
    due_date : date
    priority : PriorityEnum
    class Config:
        from_attributes = True
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
    

class TaskResponse(BaseModel):
    id : int
    title : str
    description : str
    completed : bool
    created_at : datetime
    due_date : date
    priority : PriorityEnum
    owner : UserOut

    class Config():
        from_attributes = True

class TaskOut(BaseModel):
    TaskResponse : TaskResponse

    class Config:
        from_attributes = True

class User(BaseModel):
    email : EmailStr
    password : str



class Token(BaseModel):
    access_token : str
    token_type : str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id : Optional[int] = None
    role : Optional[str] = None



    
