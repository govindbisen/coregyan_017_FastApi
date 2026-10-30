#jwt 

# header - payload - signature 


#pip install python-josh



from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

app = FastAPI()

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
security = HTTPBearer()


# Create Token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# Login API (Token Generate)
@app.post("/login")
def login(username: str, password: str):

    if username != "admin" or password != "admin1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid Username and password"
        )

    token = create_token({
        "sub": username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Token Verify
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired Token"
        )


# Protected Route
@app.get("/secure")
def secure_data(user=Depends(verify_token)):

    return {
        "message": "Secure Data Accessed",
        "user": user
    }
