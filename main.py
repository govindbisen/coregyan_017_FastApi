from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {"Hello world!!"}

@app.get('/user')
def user():
    return {"i am a user"}

@app.get('/about')
def about():
    return {"i am about"}