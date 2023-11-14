from datetime import datetime, date
import json
from tests.default_client import client
from tests.test_auth import get_valid_token

from app import schemas

base_url = "teams"
global_id = ""

def test_unauthorized():
    new_data = {}
    response = client.post(f"/{base_url}", data=json.dumps(new_data), headers={"Authorization": "Bearer TEST"})
    assert response.status_code == 401

def test_create_w_invalid_params():
    new_data = {
        "access_level":0,
        "members":[],
        "projects":[],
        "slug":"slug"
        }
    response = client.post(f"/{base_url}", data=json.dumps(new_data))
    assert response.status_code == 422

def test_delete_by_name():
    response = client.get(f"/{base_url}/slug/test-team")
    print(response)
    if response.status_code == 200:
        old_id = response.json()["_id"]
        response = client.delete(f"/{base_url}/{old_id}")
        assert response.status_code == 200
    else:
        assert response.status_code == 404

def test_create():
    global global_id
    data = {
        "name": "test_team",
    }
    response = client.post(f"/{base_url}", data=json.dumps(data))
    assert response.status_code == 200
    global_id = response.json()["_id"]
    assert global_id == response.json()["_id"]

def test_update():
    global global_id
    data = {
        "id": global_id,
        "name":"new_name",
        "slug": "new-slug"
    }
    response = client.put(f"/{base_url}", data=json.dumps(data))
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["slug"] == data["slug"]

def test_delete():
    global global_id
    response = client.delete(f"/{base_url}/{global_id}")
    assert response.status_code == 200


# def test_team_crud():
#     """This function is necessary in order to excute tests in the right order"""
#     create()
#     "..."
#     delete()
