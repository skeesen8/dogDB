from fastapi import FastAPI
from pydantic import BaseModel


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