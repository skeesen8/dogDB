from fastapi import APIRouter, Depends
from backend.models import Base, Dogs,Users
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from backend.database import get_db

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

user_db = Users

# class Userbase(BaseModel):
#     id:int
#     firstName: str | None=None
#     lastName:  str | None=None
#     userName:  str | None=None
#     password:  str | None=None
#     email:     str | None=None


userlist = []

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

# @router.get("/users/")
# async def get_users(db:user_db):
#      all_users = db.query(Users)
#      for users in all_users : userlist.append(users)
#      return userlist
     

# @app.get("/dogs/")
# async def get_dogs(db:db_dependency):
#      all_dogs = db.query(Dogs)
#      for dogs in all_dogs : dogfulllist.append(dogs)
#      return dogfulllist

# @router.post("/users/")
# async def add_user(new_user:Userbase, db:user_db):
#     db_newUser = Users(id= new_user.id,firstname = new_user.firstName,lastname = new_user.lastName,password = new_user.password,email = new_user.email)
#     db.add(db_newUser)
#     db.commit()
#     db.refresh(db_newUser)
#     return "success"

    




# @router.get("/users/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}


# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}