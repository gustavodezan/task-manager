from fastapi import HTTPException
import pytest

from app import schemas, auth, models
from tests.unit.default_db import dbs

USER_TEST_EMAIL = 'test.user.crud@test.com'
global_id = ''

# GET
def test_get_all():
    users = dbs.user.get_all()
    assert isinstance(users, list)
    for user in users:
        assert isinstance(user, models.User)

def test_get():
    users = dbs.user.get_all()
    if len(users) > 0:
        user = dbs.user.get(users[0].id)
        assert isinstance(user, models.User)
    else:
        assert users == []

def test_get_by_email():
    users = dbs.user.get_all()
    if len(users) > 0:
        user = dbs.user.get_by_email(users[0].email)
        assert isinstance(user, models.User)
    else:
        assert users == []

def test_get_for_auth():
    users = dbs.user.get_all()
    if len(users) > 0:
        user = dbs.user.get_for_auth(users[0].email)
        assert isinstance(user, schemas.UserWPass)
    else:
        assert users == []

# POST
def test_delete_for_tests():
    user = dbs.user.get_by_email(USER_TEST_EMAIL)
    if user and dbs.user.delete(user.id):
        assert True
    else:
        assert user == None

def test_create():
    global global_id

    data = schemas.UserSubmit(name="TESTE", email=USER_TEST_EMAIL, password="123456789")
    user = dbs.user.create(data)
    assert isinstance(user, schemas.User)
    assert user.email == USER_TEST_EMAIL
    assert 'password' not in user.__dict__.keys()
    global_id = user.id

def test_create_existing_email():
    data = schemas.UserSubmit(name="TESTE", email=USER_TEST_EMAIL, password="123456789")
    with pytest.raises(HTTPException) as excinfo:
        dbs.user.create(data)
    assert excinfo.errisinstance(HTTPException)

def test_create_w_wrong_schema():
    data = schemas.UserCreate(name="TESTE", email="any@any.com", password="123456789")
    with pytest.raises(HTTPException) as excinfo:
        dbs.user.create(data)
    assert excinfo.errisinstance(HTTPException)

# PUT
def test_update():
    global global_id

    data = schemas.UserUpdate(id=global_id, name="NOVO_TESTE")
    assert dbs.user.update(data)
    user = dbs.user.get(global_id)
    assert user.name == data.name
    assert user.email == USER_TEST_EMAIL

def test_not_update():
    global global_id

    data = schemas.UserUpdate(id=global_id)
    assert isinstance(dbs.user.update(data), models.User)
    user = dbs.user.get(global_id)
    assert user.name == 'NOVO_TESTE'

def test_update_w_wrong_schema():
    global global_id
    data = schemas.TeamUpdate(id=global_id, name="NEW_TEAM")
    with pytest.raises(HTTPException) as excinfo:
        user = dbs.user.update(data)
    assert excinfo.errisinstance(HTTPException)

# DELETE
def teste_delete():
    global global_id
    assert dbs.user.delete(global_id)

def test_delete_inexistent():
    global global_id
    with pytest.raises(HTTPException) as excinfo:
        dbs.user.delete(global_id)
    assert excinfo.errisinstance(HTTPException)
