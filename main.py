# TOPIC RESPONSE MODEL 

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class Product(BaseModel):
    id: int
    name: str
    price: float
    cost_price: float 
    category: str

class ProductResponse(BaseModel):
    name: str
    price: float
    category: str

# I will ont allow costprice to be displayed,  id will also not be displayed to user 
@app.get("/product",response_model = ProductResponse)
def get_product():
    return {
        "id": 101,
        "name": "Wireless Mouse",
        "price": 499.00,
        "cost_price": 250.00,  
        "category": "Electronics"
    }

# http://127.0.0.1:8000/product