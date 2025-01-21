from fastapi import APIRouter, Depends,HTTPException,status,FastAPI
from backend.models import Base, Dogs
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from backend.database import get_db
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text




# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "email": "johndoe@example.com",
#         "password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "email": "alice@example.com",
#         "password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

# class Users:
#     def __init__(self,name,id,username,password,client_id,client_secret,email,disabled):
#         self.name=name
#         self.username=username
#         self.id=id
#         self.password=password
#         self.client_id=client_id
#         self.client_secret=client_secret
#         self.email=email
#         self.disabled=disabled

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(String,nullable=False)
    password= Column(String,nullable=False)
    client_id = Column(String,nullable=False)
    client_secret = Column(String,nullable=False)
    email = Column(String,nullable=False)
    disabled = Column(Boolean, nullable=False)
    hashed_password=Column (String,nullable=False)

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
    hashed_password: str | None=None

def fake_hash_password(password: str):
    return password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return db(**user_dict)

def fake_decode_token(token):
    user = get_user(user_dependency, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict=Users.get(form_data.username)
    #fake users db used above need to use Realy Users DB but for some reason it cant access get
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # seems like my USERS db is not being accessed having to use fake db
    user = Users(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: Annotated[Userbase, Depends(get_current_user)]):
    return current_user


@router.get("/users/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# userlist = []

# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/users/")
async def add_user(new_user:Userbase, db:user_dependency):
    db_new_user = Users(
    username=new_user.username,
    hashed_password=new_user.hashed_password,
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