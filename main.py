from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()



class Product(BaseModel):
    P_ID : int
    P_NAME:str 
    P_SOLD: bool
    P_PROD_TYPE:str  

Products = [
    Product(P_ID=101, P_NAME="Wireless Mouse", P_SOLD=False, P_PROD_TYPE="Electronics"),
    Product(P_ID=102, P_NAME="Cotton Denim Jacket", P_SOLD=True, P_PROD_TYPE="Cloth"),
    Product(P_ID=103, P_NAME="Organic Almonds 500g", P_SOLD=False, P_PROD_TYPE="Food"),
    Product(P_ID=104, P_NAME="Smart Gaming Headset", P_SOLD=True, P_PROD_TYPE="Electronics")
]

@app.post("/product")
def create_product(product:Product):
    Products.append(product)
    return {"message":"Product Added","data":product}

@app.get("/product")
def getall_products():
    return {"message":"Product Added","data":Products}

@app.get("/product/{id}")
def get_product(id:int):
    for p in Products:
        print("p",p)
        if p.P_ID == id: 
            print("p.p.P_ID",id)
            return p
    return {"message" :"Not found"}

@app.put("/product/{id}")
def update_product(id:int,updated_product : Product):
    for index,product in enumerate(Products):
        if product.P_ID == id:
            Products[index] = updated_product
            return {  "message":"product Updated",
                "product": updated_product}
    return {"message" :"Not found"}
    

@app.delete("/product/{id}")
def delete_product(id:int):
    for index,product in enumerate(Products):
        if product.P_ID == id:
            Products.pop(index)
            return {"message":"data Deleted"}
    return {"message" :"Not found"}

class ProductUpdate(BaseModel):
    P_NAME: str | None = None
    P_SOLD: bool | None = None
    P_PROD_TYPE: str | None = None


@app.patch("/product/{id}")
def update_product_partial(id: int, updated_product: ProductUpdate):
    for product in Products:
        if product.P_ID == id:
            if updated_product.P_NAME is not None:
                product.P_NAME = updated_product.P_NAME
            if updated_product.P_SOLD is not None:
                product.P_SOLD = updated_product.P_SOLD
            if updated_product.P_PROD_TYPE is not None:
                product.P_PROD_TYPE = updated_product.P_PROD_TYPE
            return {
                "message": "Product partially updated",
                "product": product
            }
    return {"message": "Not found"}