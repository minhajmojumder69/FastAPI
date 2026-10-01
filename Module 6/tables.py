from database import Base
from sqlalchemy import Column,Integer,String,Boolean

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    desctiption = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean,default=False)