from fastapi import FastAPI , APIRouter,Depends, HTTPException
from pydantic import BaseModel
from tables import User
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from typing import Annotated, Optional


router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
database_dependency = Annotated[Session,Depends(get_db)]

class Users(BaseModel):
    email : str
    username : str
    firstname : str
    lastname : str
    hash_password : str
    role : str

@router.post('/creatuser')
def create_users(db : database_dependency, new_users: Users):
    user_model = User(
        email = new_users.email,
        username = new_users.username,
        firstname = new_users.firstname,
        lastname = new_users.lastname,
        hash_password = bcrypt_context.hash(new_users.password),
        is_active = True,
        role = new_users.role
    )

    db.add(user_model)
    db.commit()

    return JSONResponse(status_code= 201, content={'massage': 'User created Successfully..'})