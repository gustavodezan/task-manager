from fastapi import APIRouter, Depends
from slugify import slugify

from ..auth import CurrentUser
from .. import crud, schemas
from ..dependencies import TeamDB, UserDB


router = APIRouter()


@router.get("/all", response_model=list[schemas.Team])
def get_all_teams(user: CurrentUser, team_db: TeamDB):
    """Return all teams the user's in"""
    return team_db.get_member_teams(user.id)


@router.post("/new", response_model=schemas.TeamInDB)
def create_new_team(team: schemas.TeamCreate, user: CurrentUser, team_db: TeamDB, user_db: UserDB):
    """Create a new team"""
    slug = slugify(team.name)
    team.slug = slug
    team = schemas.TeamInDB(**team.dict(), admins=[user.id])
    team = team_db.create(team)
    return team