from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simple REST API")
port = int(os.environ.get("PORT", 8000))

# ----- Model -----
class Item(BaseModel):
    id: int
    name: str
    price: float

# ----- In-memory DB -----
items_db: List[Item] = []

# ----- Routes -----

@app.get("/")
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
    return {"message": "Item created", "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items_db
    items_db = [item for item in items_db if item.id != item_id]
    return {"message": "Item deleted"}
    
if __name__ == "__main__":
    print(f"Example app listening on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
