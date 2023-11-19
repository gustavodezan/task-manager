from datetime import datetime, date
import json
from tests.integration.default_client import client

from app import schemas

base_url = "auth"

def get_valid_token():
    data = {
        "username": "test.user@test.com",
        "password": "test_password",
        "scope": "me:read"
        }
    response = client.post(f"/{base_url}/login", data=data)
    return response.json()["access_token"]

def test_login_w_bad_structure():
    data = {
        "email": "unavailable.user@fail.com",
        "password": "wrong_password",
        "scope": "me:read"
        }
    response = client.post(f"/{base_url}/login", data=data)
    assert response.status_code == 422

def test_login_w_invalid_credentials():
    data = {
        "username": "unavailable.user@fail.com",
        "password": "wrong_password",
        "scope": "me:read"
        }
    response = client.post(f"/{base_url}/login", data=data)
    assert response.status_code == 400

def test_login():
    data = {
        "username": "test.user@test.com",
        "password": "test_password",
        "scope": "me:read"
        }
    response = client.post(f"/{base_url}/login", data=data)
    assert response.status_code == 200