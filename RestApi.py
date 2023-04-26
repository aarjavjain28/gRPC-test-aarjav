import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
