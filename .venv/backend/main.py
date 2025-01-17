from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlmodel import select, func
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.security import OAuth2PasswordBearer
from backend.config import settings
from backend.database import engine, SessionLocal 
from backend.models import Base, Dogs,Users
from backend.database import get_db
from backend.routers.users import router


def create_tables():         
	Base.metadata.create_all(bind=engine)
    

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    return app



app = start_application()

# class Userbase(BaseModel):
#     id:int
#     firstName: str | None=None
#     lastName:  str | None=None
#     userName:  str | None=None
#     password:  str | None=None
#     email:     str | None=None


class Dogbase(BaseModel):
    id: int
    name: str | None=None
    breed: str | None=None
    weight: int | None=None
    color: str |None = None

app = FastAPI()
app.include_router(router)

db_dependency = Annotated[Session, Depends(get_db)]
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




@app.get("/dogs/{dog_id}")
async def read_dog(dog_id:int, db:db_dependency):
     result = db.query(Dogs).filter(Dogs.id==dog_id).first()
     if not result:
          raise HTTPException(status_code=404,detail="no doggo found")        
     return result

@app.post("/dogs/")
async def create_dog(newdog:Dogbase, db:db_dependency):
     db_newdog=Dogs(id=newdog.id,name=newdog.name,breed=newdog.breed,weight=newdog.weight,color=newdog.color)
     db.add(db_newdog)
     db.commit()
     db.refresh(db_newdog)
     return "success"


@app.get("/dogs/")
async def get_dogs(db:db_dependency):
     dogfulllist = []
     all_dogs = db.query(Dogs)
     for dogs in all_dogs : dogfulllist.append(dogs)
     return dogfulllist

@app.delete("/dogs/{dog_id}")
async def delete_dog(dog_id:int, db:db_dependency):
     deleted_dog=db.get(Dogs,dog_id)
     # deleted_dog = db.query(Dogs).filter(Dogs.id == dog_id).all()
     if not deleted_dog:
          raise HTTPException(status_code=404,detail="cant delete object that doesnt exist") 
     db.delete(deleted_dog)
     db.commit
     db.refresh
     return f"{deleted_dog.name} has been deleted :("

@app.put("/dogs/{dog_id}")
async def update_dog(dog_id:int, name:str, breed:str, weight:int, color:str, db:db_dependency):
     db_dog = db.query(Dogs).filter(Dogs.id == dog_id).first()
     db_dog.name = name
     db_dog.breed = breed
     db_dog.weight = weight
     db_dog.color = color
     db.commit()
     return db_dog  


# app.get("/dogs/")
# async def read_users(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}