from fastapi import HTTPException
import pytest

from app import schemas, auth
from tests.unit.default_db import close_db, dbs


# GET
def test_get_all():
    users = dbs.user.get_all()
    assert isinstance(users, list)
    for user in users:
        assert isinstance(user, schemas.User)

def test_get():
    users = dbs.user.get_all()
    if len(users) > 0:
        user = dbs.user.get(users[0].id)
        assert isinstance(user, schemas.User)
        assert 'password' not in user.__dict__.keys()
    else:
        assert users == []

def test_get_by_email():
    users = dbs.user.get_all()
    if len(users) > 0:
        user = dbs.user.get_by_email(users[0].email)
        assert isinstance(user, schemas.User)
        assert 'password' not in user.__dict__.keys()
    else:
        assert users == []