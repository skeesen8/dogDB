from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlmodel import select, func
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Path, Query
from backend.config import settings
from backend.database import engine, SessionLocal 
from backend.models import Base, Dogs
from backend.database import get_db




def create_tables():         
	Base.metadata.create_all(bind=engine)
    

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()



class Dog(BaseModel):
    id: int
    name: str | None=None
    breed: str | None=None
    weight: int | None=None
    color: str |None = None

app = FastAPI()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/dogs/{dog_id}")
async def read_dog(dog_id:int, db:db_dependency):
     result = db.query(Dogs).filter(Dogs.id==dog_id).first()
     if not result:
          raise HTTPException(status_code=404,detail="no doggo found")        
     return result



    


