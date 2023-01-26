from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Tokens
class Token(BaseModel):
    access_token: str
    token_type: str
    expire: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []

class User(BaseModel):
    key: Optional[str] = None
    name: str
    email: str
    active: Optional[bool] = True
    profile_pic: Optional[bytes] = None
    register_date: Optional[str] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    teams: Optional[list[str]] = []

class UserInDB(User):
    password: str
    scopes: Optional[list[str]] = ["me:read", "me:write"]
    access_level: Optional[int] = 0

class Tag(BaseModel):
    name: str
    key: Optional[str]
    color: Optional[str] = "#000000"

class Task(BaseModel):
    name: str
    parent: str # project if root
    team: str
    key: Optional[str] = None
    create_at: Optional[str] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    due_on: Optional[str] = None
    color: Optional[str] = "#000000"
    responsibles: Optional[list[str]] = []
    tags: Optional[list[str]] = []

class Project(BaseModel):
    key: Optional[str] = None
    name: str
    team: str
    access_level: Optional[int] = 0
    color: Optional[str] = "#000000"
    status: Optional[str] = None
    tasks: Optional[list[str]] = []

class Team(BaseModel):
    key: Optional[str]
    name: str
    members: Optional[list[str]] = []
    access_level: Optional[int] = 0
    projects: Optional[list[str]] = []