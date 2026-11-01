
from fastapi import FastAPI
import time

app = FastAPI()

# Cache dictionary
cache = {}

# Cache valid for 10 seconds
CACHE_TTL = 10


# Dummy product data
products = {
    101: {"name": "Laptop", "price": 50000},
    102: {"name": "Mobile", "price": 20000}
}


@app.get("/products/{product_id}")
def get_product(product_id: int):

    # Step 1: Check whether product exists in cache
    if product_id in cache:

        cached_item = cache[product_id]

        # Step 2: Check TTL (Time To Live)
        if time.time() < cached_item["expiry"]:

            return {
                "source": "CACHE",
                "product": cached_item["data"]
            }

    # Step 3: Fetch fresh data
    product = products.get(product_id)

    if product is None:
        return {"message": "Product not found"}

    # Step 4: Store data in cache
    cache[product_id] = {
        "data": product,
        "expiry": time.time() + CACHE_TTL
    }

    # Step 5: Return fresh data
    return {
        "source": "DATABASE",
        "product": product
    }
