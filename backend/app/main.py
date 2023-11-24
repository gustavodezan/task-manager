from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from . import auth
from .router import login, user, workspaces, teams, projects, tasks, tags, auth as auth_route
from .constants import description
from .database import get_db

app = FastAPI(
    title = "Task Manager API",
    description=description
)

# cors
origins = [
    "*",
    "https://new-member-area-front.vercel.app",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000/main",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {"message":"Hi!"}

# app.include_router(login.router, prefix="/login", tags=["auth"])
app.include_router(user.router, prefix='/users', tags=['user'])
app.include_router(auth_route.router, prefix='/auth', tags=['auth'])
app.include_router(teams.router, prefix='/teams', tags=['teams'])
app.include_router(workspaces.router, prefix='/workspaces', tags=['workspaces'])
# app.include_router(projects.router, prefix="/projects", tags=["projects"], dependencies=[Depends(auth.get_current_active_user)])
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"], dependencies=[Depends(auth.get_current_active_user)])
# app.include_router(tags.router, prefix="/tags", tags=["tags"], dependencies=[Depends(auth.get_current_active_user)])
