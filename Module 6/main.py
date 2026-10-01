from fastapi import FastAPI
import tables
from database import engine

app = FastAPI()

tables.Base.metadata.create_all(bind=engine)