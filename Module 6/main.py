from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import tables
from tables import Todos
from typing import Annotated
from database import engine,SessionLocal

app = FastAPI()

tables.Base.metadata.create_all(bind=engine)

class Todo(BaseModel):
    id : int
    title : str
    desctiption : str = Field(max_length= 100)
    priority : int = Field(gt=0,lt=6)
    completed : bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
database_dependency = Annotated[Session,Depends(get_db)]

@app.get('/')
def read_todos(db : database_dependency):
    return db.query(Todos).all() 

@app.get('/todo/{todos_id}')
def read_specific_todos(db : database_dependency,todos_id = int):
    specific_todo = db.query(Todos).filter(Todos.id == todos_id).first() 
    if specific_todo is not None:
        return specific_todo
    else:
        raise HTTPException(status_code=404, detail='To do not found..') 

@app.post('/create/')
def create_todos(db : database_dependency, new_todo: Todo):
    todo_model = Todos(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()
