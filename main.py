from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Features(BaseModel):
    featureType: str
    featureTag:str

class Product(BaseModel):
    name: str
    price: int
    features:Features


@app.post("/product")
def create_product(product:Product):
    return {"message" : "product created !!" ,"product":product}
    


