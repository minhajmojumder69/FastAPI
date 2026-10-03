from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import tables
from tables import Todos
from typing import Annotated, Optional
from database import engine,SessionLocal
from fastapi.responses import JSONResponse
from router import auth

app = FastAPI()

tables.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

class Todo(BaseModel):
    id : int
    title : str
    desctiption : str = Field(max_length= 100)
    priority : int = Field(gt=0,lt=6)
    completed : bool

class Todo_update(BaseModel):
    id : Optional[int] = Field(default=None)
    title : Optional[str] = Field(default=None)
    desctiption : Optional[str] = Field(default=None,max_length= 100)
    priority : Optional[int] = Field(default=None,gt=0,lt=6)
    completed : Optional[bool]  = Field(default=None)

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
    return JSONResponse(status_code= 201, content={'massage': 'todo created Successfully..'})

@app.put('/update/{todo_id}')
def create_todos(db : database_dependency, todo_id: int, update_todo: Todo_update):

    todo = db.query(Todos).filter(Todos.id == todo_id).first() 
    if todo is None:
        raise HTTPException(status_code=404, detail='To do not found..') 

    updated = update_todo.model_dump(exclude_unset=True)

    for key,value in updated.items():
        setattr(todo,key,value)

    db.commit()
    return JSONResponse(status_code= 200, content={'massage': 'todo updated Successfully..'}) 

@app.delete('/delete/{todo_id}')
def create_todos(db : database_dependency, todo_id: int):

    todo = db.query(Todos).filter(Todos.id == todo_id).first() 
    if todo is None:
        raise HTTPException(status_code=404, detail='To do not found..') 

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
    return JSONResponse(status_code= 200, content={'massage': 'todo deleted Successfully..'}) 
