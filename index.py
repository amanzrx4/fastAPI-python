from fastapi import FastAPI, Path, HTTPException, status,Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class updateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


""" @app.get("/")
def home():
    return {'Data': 'Testing'}

@app.get("/about")
def about():
    return {'Data': 'About'} """

inventory = {}


@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The id of the item you would like to view", gt=0)):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item(name: str = Query(None, title="name", description="name of the item")):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Item id already exist")

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: updateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item id doesnt exist")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
def delele_item(item_id: int = Query(..., description="the id of the item which you wanna delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item id doesnt exist")

    del inventory[item_id]
    return {"Success": "Item deleted"}
