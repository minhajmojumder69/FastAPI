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

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
Oauth2_bearer = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = '7b3d9c2f6a9e1b4d5d0c3a6e9g8d7c6u5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d'
ALGORITHM = "HS256"

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

def authenticate_user(username,password,db):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return False
    if bcrypt_context.verify(password,user.hash_password):
        return user
    return False

def create_access_token(username:str,user_id:int,role:str,expires_delta: timedelta ):
    encode = {'sub': username,'id': user_id,'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token: Annotated[str,Depends(Oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=404,detail='User not Found')
        return {'username': username,'id': user_id,'role': role}
    except:
        raise HTTPException(status_code=404,detail='User not Found')

@router.post('/createuser')
def create_users(db : database_dependency, new_users: Users):
    user_model = User(
        email = new_users.email,
        username = new_users.username,
        firstname = new_users.firstname,
        lastname = new_users.lastname,
        hash_password = bcrypt_context.hash(new_users.hash_password),
        is_active = True,
        role = new_users.role
    )

    db.add(user_model)
    db.commit()

    return JSONResponse(status_code= 201, content={'massage': 'User created Successfully..'})

@router.post('/login')
def user_login(db: database_dependency, form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):

    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        return 'Authentication Failed'

    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {'access_token': token,'token_type':'bearer'}