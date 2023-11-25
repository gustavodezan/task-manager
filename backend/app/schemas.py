import uuid
from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field, field_validator
from slugify import slugify


class APIModel(BaseModel):
    last_modified: datetime|None = None
    created_at: datetime = Field(default_factory=datetime.now)
    # class Config:
    #     from_attributes = True

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
    project_id: int|None = None
    description: str|None = None
    parent_id: int|None = None
    due_on: datetime|None = None
    completed_at: datetime|None = None
    color: str = "#000000"
    members: list[User] = []
    subtasks: list['Task'] = []
    # tags: list[Tag] = []

class Task(TaskCreate, InDB):
    pass

class TaskUpdate(Update, InDB):
    name: str|None = None
    description: str|None = None
    due_on: datetime|None = None
    completed_at: datetime|None = None
    color: str|None = None

class ProjectCreate(APIModel):
    name: str = Field(min_length=1)
    color: str = "#000000"
    active: bool = True
    team_id: int
    tasks: list[Task] = []
    members: list[User] = []

class Project(ProjectCreate, InDB):
    pass

class ProjectUpdate(Update, InDB):
    name: str|None = None
    color: str|None = None
    status: str|None = None
    tasks: list[Task]|None = None
    admins: list[User]|None = None

class TeamBase(APIModel):
    name: str = Field(min_length=1)
    workspace_id: int
    slug: Annotated[str|None, Field(validate_default=True)] = None
    active: bool = True

    @field_validator('slug', 'name')
    @classmethod
    def validate_slug(cls, v, values) -> str:
        values = values.data
        if not v:
            return slugify(values['name'])
        return v

class TeamCreate(TeamBase):
    members: list[User|int] = []
    projects: list[Project] = []
    
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