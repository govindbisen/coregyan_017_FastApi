
# ============================================================
# JWT AUTHENTICATION USING FASTAPI
# ============================================================

# JWT = JSON WEB TOKEN
#
# JWT is used to securely transfer information between client
# and server.
#
# JWT consists of 3 parts:
#
# HEADER.PAYLOAD.SIGNATURE
#
# 1. HEADER:
#    Contains token type (JWT) and signing algorithm (HS256).
#
# 2. PAYLOAD:
#    Contains user-related information (claims).
#    Example: sub = username, exp = expiration time.
#
# 3. SIGNATURE:
#    Created using Header + Payload + SECRET_KEY.
#    It helps verify that the token was not modified.
#
# IMPORTANT:
# JWT payload is encoded, NOT encrypted.
# Never store passwords or sensitive information in JWT.


# ============================================================
# INSTALL REQUIRED PACKAGE
# ============================================================

# pip install fastapi uvicorn "python-jose[cryptography]"


# ============================================================
# IMPORTS
# ============================================================

from fastapi import FastAPI, HTTPException, Depends

# HTTPBearer:
# Extracts Bearer token from Authorization request header.
#
# HTTPAuthorizationCredentials:
# Gives access to the extracted token.
#
# Example header:
# Authorization: Bearer eyJhbGciOiJIUzI1Ni...
#
# Depends:
# Used for dependency injection in FastAPI.

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# jwt:
# Used to generate (encode) and verify (decode) JWT tokens.
#
# JWTError:
# Exception raised when JWT is invalid, expired or malformed.

from jose import jwt, JWTError

# datetime:
# Used to calculate token expiration date and time.
#
# timedelta:
# Used to add 30 minutes to current time.
#
# timezone:
# Used to generate timezone-aware UTC time.

from datetime import datetime, timedelta, timezone


# ============================================================
# FASTAPI APPLICATION
# ============================================================

# Creates the FastAPI application instance.
# All API routes will be registered using this object.

app = FastAPI()


# ============================================================
# JWT CONFIGURATION
# ============================================================

# SECRET_KEY:
# A private secret used to sign and verify JWT tokens.
#
# The same secret must be used during token creation
# and token verification.
#
# In production, store this in environment variables.
# Never expose your real secret key.

SECRET_KEY = "mysecret"


# ALGORITHM:
# HS256 = HMAC using SHA-256.
#
# This algorithm uses the same SECRET_KEY
# for signing and verifying the JWT.

ALGORITHM = "HS256"


# HTTPBearer:
# Tells FastAPI to expect a Bearer token in the
# Authorization header.
#
# Swagger UI will also show an Authorize button.
#
# HTTPBearer only extracts the token.
# It does NOT verify the JWT signature.

security = HTTPBearer()


# ============================================================
# CREATE JWT TOKEN
# ============================================================

# This function generates a JWT token.
#
# data = dictionary containing user information.
#
# Example:
# {
#     "sub": "admin"
# }
#
# sub = Subject claim.
# It identifies the user for whom the token is issued.


def create_token(data: dict):

    # Create a copy of the original dictionary.
    # We use copy() so that the original dictionary
    # does not get modified.

    to_encode = data.copy()

    # Calculate token expiration time.
    #
    # Current UTC time + 30 minutes.
    #
    # After this time, JWT verification will fail.

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    # Add expiration claim to the JWT payload.
    #
    # exp = Expiration Time.
    #
    # JWT library automatically checks this claim
    # during jwt.decode().

    to_encode.update({
        "exp": expire
    })

    # Generate JWT token.
    #
    # jwt.encode() takes 3 arguments:
    #
    # 1. to_encode  = Payload (user data + expiration)
    # 2. SECRET_KEY = Secret used for signing
    # 3. algorithm  = Signing algorithm
    #
    # It returns a JWT string:
    # HEADER.PAYLOAD.SIGNATURE

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Return the generated JWT token to the caller.

    return token


# ============================================================
# LOGIN API - GENERATE ACCESS TOKEN
# ============================================================

# POST /login
#
# Client sends username and password.
#
# Server checks credentials.
#
# If credentials are correct:
# Server generates JWT and returns it.
#
# If credentials are incorrect:
# Server returns HTTP 401 Unauthorized.

@app.post("/login")
def login(username: str, password: str):

    # DEMO ONLY:
    # Hardcoded credentials for learning JWT.
    #
    # In real applications:
    # Fetch user from database and verify hashed password.

    if username != "admin" or password != "1234":

        # HTTPException immediately stops execution
        # and sends an error response to the client.

        raise HTTPException(
            status_code=401,
            detail="Invalid Username and password"
        )

    # Credentials are correct.
    #
    # Create payload containing username.
    #
    # "sub" is a standard JWT claim.
    # It identifies the authenticated user.

    token = create_token({
        "sub": username
    })

    # Return generated JWT to the client.
    #
    # access_token = actual JWT string.
    # token_type = bearer means client should send
    # the token using Authorization: Bearer <token>.

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ============================================================
# VERIFY JWT TOKEN
# ============================================================

# This function runs whenever a protected API
# requires authentication.
#
# Depends(security):
# FastAPI first executes HTTPBearer.
#
# HTTPBearer extracts token from:
# Authorization: Bearer <JWT>
#
# credentials.credentials contains the actual JWT.


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    # Extract actual JWT string from credentials.
    #
    # credentials.scheme = "Bearer"
    # credentials.credentials = actual JWT

    token = credentials.credentials

    try:

        # Decode and verify the JWT.
        #
        # jwt.decode() performs these checks:
        #
        # 1. Verifies token signature using SECRET_KEY.
        # 2. Checks whether token has expired.
        # 3. Checks whether the signing algorithm is allowed.
        #
        # If everything is correct:
        # It returns the decoded payload dictionary.

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Return decoded payload.
        #
        # Example:
        # {
        #     "sub": "admin",
        #     "exp": 179..."
        # }
        #
        # This returned data will be available
        # inside the protected route.

        return payload

    except JWTError:

        # JWTError handles invalid JWT-related errors.
        #
        # Examples:
        # - Expired token
        # - Wrong signature
        # - Modified token
        # - Invalid token format

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired Token"
        )


# ============================================================
# PROTECTED ROUTE
# ============================================================

# GET /secure
#
# This API cannot be accessed without a valid Bearer token.
#
# Depends(verify_token):
#
# 1. FastAPI calls verify_token() before executing this route.
# 2. verify_token() extracts and verifies JWT.
# 3. If token is valid, decoded payload is returned.
# 4. That payload is injected into the user parameter.
# 5. If token is invalid, API returns HTTP 401.
#
# This is called DEPENDENCY INJECTION in FastAPI.


@app.get("/secure")
def secure_data(user=Depends(verify_token)):

    # user contains the decoded JWT payload.
    #
    # Example:
    # {
    #     "sub": "admin",
    #     "exp": 179...
    # }

    return {
        "message": "Secure Data Accessed",
        "user": user
    }


# ============================================================
# HOW TO RUN
# ============================================================

# uvicorn main:app --reload
#
# Swagger URL:
# http://127.0.0.1:8000/docs
#
# STEP 1:
# POST /login
# username = admin
# password = 1234
#
# STEP 2:
# Copy access_token from response.
#
# STEP 3:
# Click Authorize in Swagger.
# Paste the token.
#
# STEP 4:
# Execute GET /secure.
#
# EXPECTED RESPONSE:
#
# {
#     "message": "Secure Data Accessed",
#     "user": {
#         "sub": "admin",
#         "exp": 179...
#     }
# }
#
# WITHOUT TOKEN:
# HTTP 403 (HTTPBearer default behavior).
#
# WITH INVALID/EXPIRED TOKEN:
# HTTP 401.
#
# ============================================================
# END OF JWT AUTHENTICATION
# ============================================================
