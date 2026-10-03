from fastapi import FastAPI

app = FastAPI()


# path parameter  
@app.get("/user/{user_id}")
def user(user_id):
    return {f"user {user_id}"}

# path parameter with int type validation
@app.get("/product/{user_id}")
def user(user_id:int):
    return {f"user {user_id}"}



