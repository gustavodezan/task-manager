import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator
from slugify import slugify


class APIModel(BaseModel):
    last_modified: datetime|None = None
    created_at: datetime = Field(default_factory=datetime.now)
    class Config:
        from_attributes = True

class InDB(BaseModel):
    id: int

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
    name: str = Field(min_length=1)
    email: str

class UserCreate(UserBase):
    password: str = Field(max_length=64, min_length=8)

class User(UserBase):
    active: bool = True
    profile_pic: str|None = None
    # scopes: list[str] = ["me:read", "me:write"]
    access_level: int = 0

class UserSubmit(User, UserCreate):
    pass

class UserInDB(User, InDB):
    pass

class UserWPass(UserInDB, UserCreate):
    pass

class UserShort(UserBase, InDB):
    profile_pic: str|None = None

class UserUpdate(Update):
    id: int
    name: str|None = None
    active: str|None = None
    profile_pic: str|None = None
    access_level: int|None = None

class Tag(APIModel):
    id: int = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(min_length=1)
    color: str = "#000000"


class TaskCreate(APIModel):
    name: str = Field(min_length=1)
    parent_id: int|None
    due_on: datetime|None = None
    completed_at: datetime|None = None
    color: str = "#000000"
    members: list[User]
    tags: list[Tag]

class Task(TaskCreate, InDB):
    pass

class TaskInDB(Task, InDB):
    pass

class ProjectCreate(APIModel):
    name: str = Field(min_length=1)
    color: str = "#000000"
    active: bool = True
    tasks: list[Task]
    members: list[User]

    team_id: int

class Project(ProjectCreate, InDB):
    pass

class ProjectUpdate(Update):
    name: str|None = None
    color: str|None = None
    status: str|None = None
    tasks: list[Task]|None = None
    admins: list[User]|None = None

class TeamBase(APIModel):
    name: str = Field(min_length=1)
    workspace_id: int
    slug: str|None = None
    active: bool = True

class TeamCreate(TeamBase):
    members: list[User|int] = []
    projects: list[Project] = []

    @validator('slug', always=True)
    def ab(cls, v, values) -> str:
        if not v:
            return slugify(values['name'])
        return v

class Team(TeamCreate):
    admins: list[User]|list[str] = []

class TeamInDB(Team, InDB):
    pass

class TeamUpdate(Update):
    id: int
    name: str|None = None
    access_level: int|None = None
    members: list[int]|None = None
    projects: list[Project]|None = None
    slug: str|None = None

class TeamShort(TeamBase, InDB):
    pass

class WorkspaceBase(APIModel):
    name: str = Field(min_length=1)

class Workspace(WorkspaceBase):
    members: list[User] = []
    teams: list[Team] = []
    # projects: list[Project] = []

class WorkspaceInDB(Workspace,InDB):
    pass

class WorkspaceShort(WorkspaceBase, InDB):
    pass

class WorkspaceUpdate(Update):
    id: int
    name: str|None = None
    members: list[User]|None = None
    owners: list[User]|None = None
    teams: list[Team]|None = None


class UserResponse(UserInDB):
    teams: list[TeamShort]

class TeamResponse(TeamShort, InDB):
    pass