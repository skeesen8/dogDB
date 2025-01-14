from backend.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class Dogs(Base):
    __tablename__ = "dogs"
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    breed = Column(String,nullable=False)
    weight = Column(Integer,nullable=False)
    color = Column(String,nullable=False)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    firstName = Column(String,nullable=False)
    lastName= Column(String,nullable=False)
    userName = Column(String,nullable=False)
    password = Column(String,nullable=False)
    email = Column(String,nullable=False)