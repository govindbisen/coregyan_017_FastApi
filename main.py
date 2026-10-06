from fastapi import FastAPI, HTTPException, status, Request,Depends
from fastapi.responses import JSONResponse
from typing import Annotated
app = FastAPI()

items = {"1": "Laptop", "2": "Smartphone"}


# dependency injection 

def commonLogig():
    return "this is dependency injection of common logic"



#1 Depends
@app.get("/item/{item_id}")
# def read_item(item_id: str, data = Depends(commonLogig)):   
def read_item(item_id: str ,data: Annotated[str, Depends(commonLogig)] ): # modern way 
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item not found in ji jo karna hai kar lo.."
        )
    return {"item": items[item_id] , "depoutput" :data}

