from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#A decorator is a function that modifies or extends the behavior of another function without changing its original code.
#Pydantic is a Python library used for data validation and parsing using Python type hints.

class Product(BaseModel):
    name:str
    price:int

@app.post("/product")
def product(product:Product):
    return {"Message":f"product created name : {product.name} with Price : {product.price} "}

