from backend.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    breed = Column(String,nullable=False)
    weight = Column(Integer, nullable=False)
    color = Column(String, nullable=False)

    