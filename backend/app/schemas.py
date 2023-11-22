import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator
from slugify import slugify


class APIModel(BaseModel):
    last_modified: datetime|None = None
    pass

class InDB(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")

class Update(APIModel):
    last_modified: datetime = Field(default_factory=datetime.now)

# Tokens
class Token(APIModel):
    access_token: str
    token_type: str
    expire: int

class TokenData(APIModel):
    username: str|None = None
    scopes: list[str]


class UserBase(APIModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str = Field(max_length=64, min_length=8)

class User(UserBase, InDB):
    active: bool = True
    profile_pic: str|None = None
    register_date: datetime = Field(default_factory=datetime.now)
    # teams: list["Team"] = []
    # scopes: list[str] = ["me:read", "me:write"]
    access_level: int = 0

class UserInDB(User,UserCreate):
    pass

class UserUpdate(Update):
    id: str
    name: str|None = None
    active: str|None = None
    profile_pic: str|None = None
    access_level: int|None = None

class Tag(APIModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    color: str = "#000000"


class TaskCreate(APIModel):
    name: str
    parent: str # project if root
    created_at: datetime = Field(default_factory=datetime.now)
    due_on: datetime|None = None
    completed_at: datetime|None = None
    color: str = "#000000"
    responsibles: list[User]
    tags: list[Tag]

class Task(TaskCreate, InDB):
    pass

class ProjectCreate(APIModel):
    name: str
    access_level: int = 0
    color: str = "#000000"
    status: str|None = None
    tasks: list[Task]
    admins: list[User]

class Project(ProjectCreate, InDB):
    pass

class ProjectUpdate(Update):
    name: str|None = None
    color: str|None = None
    status: str|None = None
    tasks: list[Task]|None = None
    admins: list[User]|None = None

class TeamCreate(APIModel):
    name: str
    access_level: int = 0
    members: list[User]|list[str] = []
    projects: list[Project] = []
    slug: str|None = None

    @validator('slug', always=True)
    def ab(cls, v, values) -> str:
        if not v:
            return slugify(values['name'])
        return v

class Team(TeamCreate):
    admins: list[User]|list[str] = []

class TeamInDB(Team):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")

class TeamUpdate(Update):
    id: str
    name: str|None = None
    access_level: int|None = None
    members: list[User]|list[str]|None = None
    projects: list[Project]|None = None
    slug: str|None = None

class Workspace(APIModel):
    name: str
    members: list[User] = []
    owners: list[User] = []
    teams: list[Team] = []
    # projects: list[Project] = []

class WorkspaceInDB(InDB):
    pass

class WorkspaceUpdate(Update):
    name: str|None = None
    members: list[User]|None = None
    owners: list[User]|None = None
    teams: list[Team]|None = None