# import time;
# import asyncio;


# def task():
#     time.sleep(3000)
#     return "Done"


# async def task():
#     await asyncio.sleep(3)
#     return "Done"


import asyncio;
from fastapi import FastAPI;

app = FastAPI()

@app.get("/")
async def home():
    await asyncio.sleep(3);
    return "Done api ran and returned the respnose after 3 second!!"