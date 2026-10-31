
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Read .env file
from dotenv import load_dotenv

# Access environment variables
import os

app = FastAPI()


# STEP 1: Load .env file
load_dotenv()


# STEP 2: Read frontend URL from environment
FRONTEND_URL = os.getenv("FRONTEND_URL")


# STEP 3: Allowed origins
origins = [
    FRONTEND_URL
]


# STEP 4: Configure CORS middleware
app.add_middleware(
    CORSMiddleware,

    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# STEP 5: Home API
@app.get("/")
def home():
    return {
        "message": "CORS ENABLE API",
        "frontend": FRONTEND_URL
    }
