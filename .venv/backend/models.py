from backend.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class Dogs(Base):
    __tablename__ = "dogs"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    breed = Column(String,nullable=False)
    weight = Column(Integer, nullable=False)
    color = Column(String, nullable=False)

    