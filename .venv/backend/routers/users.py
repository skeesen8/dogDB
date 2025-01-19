from fastapi import APIRouter, Depends,HTTPException,status,FastAPI
from backend.models import Base, Dogs,Users
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from backend.database import get_db


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "password": "fakehashedsecret2",
        "disabled": True,
    },
}


user_db = Users

router = APIRouter()
user_dependency = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Userbase(BaseModel):
    id:int
    client_id: int | None=None
    client_secret:int | None=None
    username:  str | None=None
    password:  str | None=None
    email:     str | None=None
    disabled: bool | None=None

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    return Users(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@router.post("/token")
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],db:user_dependency):
    user_dict=fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = Users(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: Annotated[Users, Depends(get_current_user)]):
    return current_user


@router.get("/users/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# userlist = []

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/users/")
async def add_user(new_user:Userbase, db:user_dependency):
    db_new_user = Users(
    username=new_user.username,
    id= new_user.id,
    password = new_user.password,
    email = new_user.email,
    client_id=new_user.client_id,
    client_secret=new_user.client_secret,
    disabled=new_user.disabled)
    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)
    return "success"

    




# @router.get("/users/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}


# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}