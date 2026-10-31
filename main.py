from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Frontend origins allowed to access this API
    allow_origins=["http://localhost:3000"],
    
    # Allow cookies and authentication credentials
    allow_credentials=True,

    # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],

    # Allow all request headers
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "CORS enabled"}