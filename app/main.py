from fastapi import FastAPI
from .routers import task,user,oauth
from . import models
from .database import Base,engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(oauth.router)

@app.get('/')
def get_hello():
    return {"message":"Hello world"}