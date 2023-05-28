from fastapi import APIRouter, Depends
from ..auth import get_current_active_user
from .. import crud
from ..schemas import Team, User


router = APIRouter()


@router.get("/my-teams", response_model=list[Team])
def get_all_teams(user: User = Depends(get_current_active_user)):
    """Return all teams the user's in"""
    return crud.Team.fetch({"members?contains": user.key})

# @router.post("/create", response_model=Team)
# def create_new_team(team: Team, user: User = Depends(get_current_active_user)):
#     """Create a new team"""
#     if user.key not in team.members:
#         team.members.append(user.key)
#     new_team = crud.Team.create(team.dict())
#     user = crud.User.get_raw(user.key)
#     user['teams'].append(new_team['key'])
#     crud.User.update(user)
#     return new_team

# @router.put("update", response_model=Team)
# def create_new_team(team: Team):
#     """Update team info"""
#     return crud.Team.update(team)