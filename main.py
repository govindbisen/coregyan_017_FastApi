from fastapi import FastAPI, HTTPException,Header, status, Request,Depends
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"1": "Laptop", "2": "Smartphone"}


# dependency injection EG 1 

def commonLogig():
    return "this is dependency injection of common logic"



#1 Depends 
@app.get("/item/{item_id}")
def read_item(item_id: str, data = Depends(commonLogig)):
   
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item not found in ji jo karna hai kar lo.."
        )
    return {"item": items[item_id] , "depoutput" :data}



# practicle use EG 2 

SECRET_TOKEN = "mysecrettoken"
# REQUEST ME Authorization: Bearer mysecrettoken

def verify_token(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing"
        )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return {
        "user": "Authorized User"
    }


@app.get("/secure-data")
def secure_data(user: dict = Depends(verify_token)):
    return {
        "message": "Secure data accessed successfully",
        "user": user
    }

