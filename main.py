from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# 1. "user_id" is declared in the path, so it's a Path Parameter
# 2. "role" and "limit" are not in the path, so they are Query Parameters
@app.get("/users/{user_id}/items")
async def get_user_items(
    user_id: int,                   # Path param (Required)
    role: Optional[str] = None,     # Query param (Optional, defaults to None)
    limit: int = 10                 # Query param (Optional, defaults to 10)
):
    return {
        "user_id": user_id,
        "applied_filter_role": role,
        "limit_results": limit,
        "message": f"Fetching {limit} items for user {user_id} filtered by {role}"
    }
