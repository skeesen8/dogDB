from fastapi import FastAPI
from pydantic import BaseModel


class Dog(BaseModel):
    id: int
    name: str | None=None
    breed: str | None=None
    weight: int | None=None
    color: str |None = None


app = FastAPI()






@app.get("/")
async def root():
    return {"message": "Hello World"}