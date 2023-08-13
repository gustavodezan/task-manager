from typing import Annotated
from fastapi import Depends
from . import crud

UserDB = Annotated[crud.User, Depends(crud.User)]
TeamDB = Annotated[crud.Team, Depends(crud.Team)]