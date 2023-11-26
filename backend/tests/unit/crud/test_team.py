# from fastapi.testclient import TestClient
from fastapi import HTTPException
import sqlalchemy.exc
import pytest

from app import schemas, models
from tests.unit.default_db import dbs


# GET
def test_get_all():
    teams = dbs.team.get_all()
    assert isinstance(teams, list)
    for team in teams:
        assert isinstance(team, models.Team)

def test_get():
    teams = dbs.team.get_all()
    if len(teams) > 0:
        team = dbs.team.get(teams[0].id)
        assert isinstance(team, models.Team)
    else:
        assert teams == []

def test_get_inexistent():
    not_team = dbs.team.get(-1)
    assert not_team == None

# def test_get_wrong_type():
#     with pytest.raises(sqlalchemy.exc.DataError) as excinfo:
#         not_team = dbs.team.get('oi')
#         # assert not_team == None
#     assert excinfo.errisinstance(sqlalchemy.exc.DataError)

def test_get_by_slug():
    teams = dbs.team.get_all()
    if len(teams) > 0:
        team = dbs.team.get_by_slug(teams[0].slug)
        assert isinstance(team, models.Team)
    else:
        assert teams == []

def test_get_by_slug_inexistent():
    team = dbs.team.get_by_slug("")
    assert team == None

def test_get_member_teams():
    test_user_id = 2
    teams = dbs.team.get_member_teams(test_user_id)
    assert isinstance(teams, list)
    for team in teams:
        assert isinstance(team, models.Team)
        assert test_user_id in [m.id for m in team.members]

def test_get_member_teams_member_invalid_user():
    test_user_id = -1
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

    data = schemas.TeamCreate(name="test_crud_team", workspace_id=1)
    team = dbs.team.create(data)
    assert isinstance(team, models.Team)
    assert team.name == data.name
    assert team.slug == data.slug
    global_id = team.id

# def test_create_wo_name():
#     with pytest.raises(HTTPException) as excinfo:
#         team = dbs.team.create(schemas.TeamCreate(name="", workspace_id=1))
#     assert excinfo.errisinstance(HTTPException)
    
#     with pytest.raises(HTTPException) as excinfo:
#         team = schemas.Team(name="name")
#         team = dbs.team.create(team)
#     assert excinfo.errisinstance(HTTPException)
    
    
    
# PUT
# @pytest.mark.skip()
def test_update():
    global global_id

    data = schemas.TeamUpdate(id=global_id, name="new name old-slug")
    team = dbs.team.update(data)
    assert team.name == data.name
    assert team.slug != None

def test_not_update():
    global global_id

    _team = dbs.team.get(global_id)
    data = schemas.TeamUpdate(id=global_id)
    team = dbs.team.update(data)

    assert team.name == _team.name
    assert team.slug == _team.slug


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