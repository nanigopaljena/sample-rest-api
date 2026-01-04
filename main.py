from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simple REST API")

class Item(BaseModel):
    id: int
    name: str
    price: float

items_db: List[Item] = []

@app.api_route("/", methods=["GET", "HEAD"])
def health():
    return {"status": "UP"}

@app.get("/items")
def get_items():
    return items_db

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}

@app.post("/items")
def create_item(item: Item):
    items_db.append(item)
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return {"message": "Item deleted"}
