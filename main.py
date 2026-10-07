import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    # Response milne ke baad total time calculate
    response = await call_next(request)
    # Response milne ke baad total time calculate
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.get("/test")
async def root():
    return {"message": "Hello World"}

# Client Request → Middleware (Start Time) → Route Logic → Middleware (Calculate Time + Add Header) → Client Response