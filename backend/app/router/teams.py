from fastapi import APIRouter, Depends
from slugify import slugify

from ..auth import CurrentUser
from .. import crud, schemas
from ..dependencies import TeamDB, UserDB, GetDBs
from .. import exceptions


router = APIRouter()


@router.get("/slug/{team_slug}", response_model=schemas.TeamResponse)
def get_team_by_slug(team_slug: str, user: CurrentUser, dbs: GetDBs):
    team = dbs.team.get_by_slug(team_slug)
    if not team:
        raise exceptions.not_found("Team")
    
    if team not in user.teams:
        print(1)
    else:
        print(2)

    return team

@router.get("/{team_id}", response_model=schemas.TeamResponse)
def get_all_teams_of_user(team_id: int, team_db: TeamDB):
    """Return all teams the user's in"""
    # return team_db.get_all()
    team = team_db.get(team_id)
    if not team:
        raise exceptions.not_found("Team")
    return team

@router.get("/", response_model=list[schemas.TeamShort])
def get_all_teams_of_user(team_db: TeamDB, user: CurrentUser):
    """Return all teams the user's in"""
    return team_db.get_all()
    return team_db.get_member_teams(user.id)

@router.post("/")
def create_new_team(team: schemas.TeamCreate, dbs: GetDBs):
    """Create a new team"""
    slug = slugify(team.name)
    team.slug = slug
    # team = schemas.TeamCreate(**team.model_dump())
    members = []
    for member in team.members:
        if type(member) != int:
            continue
        _user = dbs.user.get(member, validate=False)
        if _user:
            members.append(_user)

    team.members = members
    team = dbs.team.create(team)
    # team = dbs.team.add_members(team.id, members)
    return team

@router.put("/add")#, response_model=schemas.TeamInDB
def manage_team_members(add_members: schemas.TeamAddMembers, user: CurrentUser, dbs: GetDBs):
    """Update team data"""
    team = dbs.team.get(add_members.id)
    if not team:
        raise exceptions.not_found("Team")
    
    members = []
    for member_id in add_members.members:
        member = dbs.user.get(member_id)
        if member:
            members.append(member)
    add_members.members = members

    new_team = dbs.team.update(add_members)
    return new_team

@router.put("/")#, response_model=schemas.TeamInDB
def update_team_data(team: schemas.TeamUpdate, user: CurrentUser, dbs: GetDBs):
    """Update team data"""
    _team = dbs.team.get(team.id)
    if not _team:
        raise exceptions.not_found("Team")
    
    # if user.id not in _team.admins:
    #     raise exceptions.not_enough_permissions()
    new_team = dbs.team.update(team)
    return new_team

@router.delete("/{team_id}")
def delete_team(team_id: str, user: CurrentUser, dbs: GetDBs):
    """Delete specified team"""
    # if user.access_level < x
    return dbs.team.delete(team_id)
