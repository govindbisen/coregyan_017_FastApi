
# Import FastAPI to create our backend application
# Import HTTPException to handle and return HTTP errors
from fastapi import FastAPI, HTTPException

# Import httpx to make asynchronous HTTP requests
import httpx


# Create FastAPI application instance
app = FastAPI()


# =====================================================
# Example 1: JSONPlaceholder - Get All Users
# =====================================================

# Define GET endpoint: http://127.0.0.1:8000/users
@app.get("/users")
async def get_users(page:int = 1):

    try:

        # AsyncClient creates an HTTP client to communicate
        # with an external API.
        #
        # async with automatically closes the client
        # after the request is completed.
        async with httpx.AsyncClient() as client:

            # Send GET request to JSONPlaceholder API.
            #
            # await is used because the HTTP request is asynchronous.
            # It allows the event loop to handle other tasks
            # while waiting for the external API response.
            response = await client.get(
                "https://jsonplaceholder.typicode.com/users"
            )

            # Check HTTP response status.
            # If status is 4xx or 5xx, HTTPStatusError is raised.
            response.raise_for_status()

            # Convert JSON response into Python data
            # (list or dictionary) and return it to the client.

            # pagination 

            limit = 3 
            # page = 1
            start =( page - 1 )*limit
            end = start + limit 
            return response.json()[start:end]

    # RequestError handles network-related errors,
    # connection failures and timeout errors.
    except httpx.RequestError:

        # 502 means our server received a failure
        # while communicating with the external API.
        raise HTTPException(
            status_code=502,
            detail="External API connection failed"
        )

    # HTTPStatusError occurs when external API
    # returns an unsuccessful HTTP status (4xx or 5xx).
    except httpx.HTTPStatusError:

        raise HTTPException(
            status_code=502,
            detail="External API error"
        )

