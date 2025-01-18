from fastapi import APIRouter, Depends
from backend.models import Base, Dogs,Users
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from backend.database import get_db

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    return Users(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@router.get("/users/me")
async def read_users_me(current_user: Annotated[Users, Depends(get_current_user)]):
    return current_user


@router.get("/users/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

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