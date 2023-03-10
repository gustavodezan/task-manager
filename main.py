from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from router import login, user, teams, projects, tasks, tags
from app import auth
from app.description import description

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

app.include_router(login.router, prefix="/login", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"], dependencies=[Depends(auth.get_current_active_user)])
app.include_router(teams.router, prefix="/teams", tags=["teams"], dependencies=[Depends(auth.get_current_active_user)])
app.include_router(projects.router, prefix="/projects", tags=["projects"], dependencies=[Depends(auth.get_current_active_user)])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"], dependencies=[Depends(auth.get_current_active_user)])
app.include_router(tags.router, prefix="/tags", tags=["tags"], dependencies=[Depends(auth.get_current_active_user)])
