from fastapi import FastAPI , APIRouter,Depends, HTTPException
from pydantic import BaseModel
from tables import User
from datetime import timedelta, datetime,timezone
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt
from router.auth import get_current_user
from tables import Todos

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
database_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@router.get('/admin/todos')
def read_todos(user: user_dependency,db : database_dependency):

    if user is None or user.get('role') != 'admin':
            raise HTTPException(status_code=401,detail="Failed Authentication")

    return db.query(Todos).all()

@router.delete('/admin/delete/{todo_id}')
def delete_todos_by_admin(user: user_dependency,db : database_dependency, todo_id: int):

    if user is None or user.get('role' != 'admin'):
        raise HTTPException(status_code=401,detail="Failed Authentication")

    todo = db.query(Todos).filter(Todos.id == todo_id).first() 
    if todo is None:
        raise HTTPException(status_code=404, detail='To do not found..') 

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
    return JSONResponse(status_code= 200, content={'massage': 'todo deleted Successfully..'})