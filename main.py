from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"1": "Laptop", "2": "Smartphone"}



#1  simple http exception
@app.get("/item/{item_id}")
def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item not found in ji jo karna hai kar lo.."
        )
    return {"item": items[item_id]}


#2  Global Exception Handling 

# Consistent Responses	All errors follow the same format
# Security	No stack traces or internal details exposed
# Debugging	Centralized logging of all errors
# User Experience	Clear, actionable error messages
# Maintenance	Single place to update error handling logic

# If you have custom application errors (e.g., a database connection failure, a payment error, or an internal domain exception), 
# you can map those Python classes to global API responses using the @app.exception_handler decorator.
# This keeps your route functions clean because you don't have to write try-except blocks inside every single endpoint.

# custom exception 
class ItemNotFoundException(Exception):
    def __init__(self,message:str):
        self.message = message

# 2. Global Exception Handler Register Karo
@app.exception_handler(ItemNotFoundException)
async def global_item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )

@app.get("/item/cust/{item_id}")
def read_item(item_id: str):
    if item_id not in items:
        raise ItemNotFoundException(message="Item not found in jo jo karna hai kar lo..")
    return {"item": items[item_id]}


#3 3. Overriding Built-in FastAPI Request Validation Errors
# FastAPI automatically throws a validation error (422 Unprocessable Entity) if a client sends the wrong data type (e.g., passing a string into a path parameter that expects an integer).
# If you don't like FastAPI's default error format, you can override its built-in handler (RequestValidationError) to format the JSON response exactly how you or your frontend team wants it.