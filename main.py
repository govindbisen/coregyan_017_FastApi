
from fastapi import FastAPI

app = FastAPI()


# API 1: Hello World
@app.get("/")
def home():
    return {
        "message": "Hello World"
    }


# API 2: Addition
@app.get("/add")
def addition(a: int, b: int):

    return {
        "result": a + b
    }
