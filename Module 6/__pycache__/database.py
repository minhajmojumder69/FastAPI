from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:Password@localhost/TodoApplicationDataBase'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:password@127.0.0.1:3306/TodoAppllicatiionDatabase'
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres.oaaqakhnugiwioncdozq:LogicHunters190@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)

Base = declarative_base()
