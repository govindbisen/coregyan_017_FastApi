# middleware 

from fastapi import FastAPI, Depends, Request, HTTPException, status
import time

app = FastAPI()

@app.middleware("http")
async def global_timer_middleware(request: Request, call_next):
    # This fires for /health, /users, /docs, and everything else blindly.
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Global-Latency"] = f"{process_time:.4f}s"
    print("just priniting before test")
    return response

@app.get("/test")
def test():
    return "test response"