from fastapi import APIRouter, Depends
from slugify import slugify

from ..auth import CurrentUser
from .. import crud, schemas
from ..dependencies import TeamDB, UserDB, GetDBs
from .. import exceptions


router = APIRouter()


@router.get("/slug/{team_slug}")
def get_team_by_slug(team_slug: str, dbs: GetDBs):
    team = dbs.team.get_by_slug(team_slug)
    if not team:
        raise exceptions.not_found("Team")
    return team

@router.get("/", response_model=list[schemas.TeamInDB])
def get_all_teams_of_user(user: CurrentUser, team_db: TeamDB):
    """Return all teams the user's in"""
    return team_db.get_all()
    return team_db.get_member_teams(user.id)

@router.post("/", response_model=schemas.TeamInDB)
def create_new_team(team: schemas.TeamCreate, user: CurrentUser, dbs: GetDBs):
    """Create a new team"""
    slug = slugify(team.name)
    team.slug = slug
    team = schemas.TeamInDB(**team.model_dump(), admins=[user.id])
    team = dbs.team.create(team)
    return team

@router.put("/")#, response_model=schemas.TeamInDB
def update_team_data(team: schemas.TeamUpdate, user: CurrentUser, dbs: GetDBs):
    """Update team data"""
    _team = dbs.team.get(team.id)
    if not _team:
        raise exceptions.not_found("Team")
    
    if user.id not in _team.admins:
        raise exceptions.not_enough_permissions()
    if dbs.team.update(team):
        new_team = dbs.team.get(team.id)
        return new_team
    raise exceptions.internal_error()

@router.delete("/{team_id}")
def delete_team(team_id: str, user: CurrentUser, dbs: GetDBs):
    """Delete specified team"""
    # if user.access_level < x
    return dbs.team.delete(team_id)
