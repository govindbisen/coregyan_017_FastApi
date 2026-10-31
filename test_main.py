
# Import TestClient for testing FastAPI APIs
from fastapi.testclient import TestClient

# Import our FastAPI application
from main import app

# Create test client
client = TestClient(app)


# TEST 1: Hello World API
def test_home():

    # Send GET request to home API
    response = client.get("/")

    # Check HTTP status code
    assert response.status_code == 200

    # Check API response data
    assert response.json() == {
        "message": "Hello World"
    }


# TEST 2: Addition API
def test_addition():

    # Send GET request with query parameters
    response = client.get("/add?a=10&b=20")

    # Check HTTP status code
    assert response.status_code == 200

    # Check addition result
    assert response.json() == {
        "result": 30
    }
