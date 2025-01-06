from fastapi import FastAPI
from pydantic import BaseModel

from fastapi import FastAPI
from backend.config import settings
from backend.session import engine 
from backend.models import Base

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

@app.get("/dog/{Dog_id}")
async def get_dogs():
    return {"message": "Hello World"}

@app.post("/dogs")
async def create_dog(dog: Dog):
    return dog