# from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest

from app import schemas
from tests.unit.default_db import dbs


# GET
def test_get_all():
    teams = dbs.team.get_all()
    assert isinstance(teams, list)
    for team in teams:
        assert isinstance(team, schemas.TeamInDB)

def test_get():
    teams = dbs.team.get_all()
    if len(teams) > 0:
        team = dbs.team.get(teams[0].id)
        assert isinstance(team, schemas.TeamInDB)
    else:
        assert teams == []

def test_get_inexistent():
    not_team = dbs.team.get("id")
    assert not_team == None

def test_get_wrong_type():
    not_team = dbs.team.get(1)
    assert not_team == None

def test_get_by_slug():
    teams = dbs.team.get_all()
    if len(teams) > 0:
        team = dbs.team.get_by_slug(teams[0].slug)
        assert isinstance(team, schemas.TeamInDB)
    else:
        assert teams == []

def test_get_by_slug_inexistent():
    team = dbs.team.get_by_slug("")
    assert team == None

def test_get_member_teams():
    test_user_id = "75e9d16c-2aec-4375-a6fb-1996665dbf2b"
    teams = dbs.team.get_member_teams(test_user_id)
    assert isinstance(teams, list)
    for team in teams:
        assert isinstance(team, schemas.TeamInDB)
        assert test_user_id in team.members

def test_get_member_teams_member_invalid_user():
    test_user_id = "id"
    teams = dbs.team.get_member_teams(test_user_id)
    assert teams == []

# POST
global_id = ''

def test_delete_test_team():
    team = dbs.team.get_by_slug("test-crud-team")
    if team:
        status = dbs.team.delete(team.id)
        assert status == True
    else:
        assert team == None

def test_create():
    global global_id

    data = schemas.TeamInDB(name="test_crud_team")
    team = dbs.team.create(data)
    assert isinstance(team, schemas.TeamInDB)
    assert team.name == data.name
    assert team.slug == data.slug
    global_id = team.id

def test_create_wo_name():
    with pytest.raises(HTTPException) as excinfo:
        team = dbs.team.create({})
    assert excinfo.errisinstance(HTTPException)
    
    with pytest.raises(HTTPException) as excinfo:
        team = schemas.Team(name="name")
        team = dbs.team.create(team)
    assert excinfo.errisinstance(HTTPException)
    
    
    
# PUT
# @pytest.mark.skip()
def test_update():
    global global_id

    data = schemas.TeamUpdate(id=global_id, name="new name old-slug")
    if dbs.team.update(data):
        team = dbs.team.get(global_id)
        assert team.name == data.name
        assert team.slug != None
    else:
        team = dbs.team.get(global_id)
        raise RuntimeError

def test_not_update():
    global global_id

    data = schemas.TeamUpdate(id=global_id)
    if dbs.team.update(data):
        raise RuntimeError
    else:
        team = dbs.team.get(global_id)
        assert team.name != None
        assert team.slug != None


# DELETE
def test_delete():
    global global_id
    assert dbs.team.delete(global_id)

def test_delete_inexistent():
    global global_id
    with pytest.raises(HTTPException) as excinfo:
        dbs.team.delete(global_id)
    assert excinfo.errisinstance(HTTPException)

# def test_close_db():
#     close_db()