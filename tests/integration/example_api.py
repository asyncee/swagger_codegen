import datetime as dt
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/get", operation_id="get_simple", response_model=Dict[str, str])
def get():
    return {"Hello": "World"}


@app.post("/post/simple", operation_id="post_simple", response_model=int)
def post_simple(number: int):
    return number


class PostDTO(BaseModel):
    string: str
    number: int
    date: dt.date
    datetime: dt.datetime


@app.post("/post/dto", operation_id="post_dto", response_model=PostDTO)
def post_dto(payload: PostDTO):
    return payload.dict()
