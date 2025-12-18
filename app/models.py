from sqlalchemy import Integer,String,Boolean,Column,ForeignKey,Date
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as sqlEnum
from .enum import PriorityEnum

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    completed = Column(Boolean,server_default='False')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    due_date = Column(Date,nullable=False)
    priority = Column(sqlEnum(PriorityEnum),nullable=False)
    owner = relationship('User')

class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
