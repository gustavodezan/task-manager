from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import json


client = TestClient(app)

def get_valid_token():
    data = {
        "username": "test.user@test.com",
        "password": "test_password",
        "scope": "me:read"
        }
    response = client.post(f"/auth/login", data=data)
    return response.json()["access_token"]

client.headers = {"Authorization": f"Bearer {get_valid_token()}"}