from typing import Annotated
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from . import schemas
from .dependencies import GetDB
from .exceptions import not_found, already_exists

class Crud:
    def __init__(self, db: GetDB):
        self.db = db

class User(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.db = db.user
        # self.db.drop()

    def get(self, user_id: str):
        return self.db.find_one({"_id":user_id})
    
    def get_by_email(self, email: str):
        return self.db.find_one({"email":email})
    
    def get_all(self):
        return list(self.db.find())

    def create(self, user: schemas.User):
        if self.get_by_email(user.email):
            raise already_exists("User")
        user = jsonable_encoder(user)
        new_user = self.db.insert_one(user)
        return self.get(new_user.inserted_id)

class Team(Crud):
    def __init__(self, db: GetDB):
        super().__init__(db)
        self.db = db.team
    
    def get(self, team_id: int):
        return self.db.find_one({"_id": team_id})
    
    def get_by_slug(self, slug: str):
        return self.db.find_one({"slug": slug})
    
    def get_all(self):
        return list(self.db.find())
    
    def create(self, team: schemas.Team):
        if self.get_by_slug(team.slug):
            raise already_exists("Team with that name")
        team = jsonable_encoder(team)
        new_team = self.db.insert_one(team)
        return self.get(new_team.inserted_id)

UserDB = Annotated[User, Depends(User)]
TeamDB = Annotated[Team, Depends(Team)]

