from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get('/')
def home():
    return {"Hello world!!"}

# Query params
@app.get('/user')
def user(name:str):
    return {f"hello {name}!!"}

# Query params with optional productname   

# http://127.0.0.1:8000/product?productname=prd1
@app.get('/product')
def product(productname: str = None):
    return {"message": f"hello {productname}!!"}


# Query params with multiple params

# http://127.0.0.1:8000/items?limit=10&offset=20&itemtype=cloth
@app.get('/items')
def item(limit:int , offset:int, itemtype:str):
    return {"message for ":itemtype, "limit":limit,"offset":offset}