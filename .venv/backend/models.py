from backend.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class Dogs(Base):
    __tablename__ = "dogs"
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    breed = Column(String,nullable=False)
    weight = Column(Integer,nullable=False)
    color = Column(String,nullable=False)

# class Users(Base):
#     __tablename__ = "users"
#     id = Column(Integer,primary_key=True,nullable=False)
#     username = Column(String,nullable=False)
#     password= Column(String,nullable=False)
#     client_id = Column(String,nullable=False)
#     client_secret = Column(String,nullable=False)
#     email = Column(String,nullable=False)
#     disabled = Column(Boolean, nullable=False)
#     hashed_password=Column (String,nullable=False)

    