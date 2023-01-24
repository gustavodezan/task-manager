from fastapi import FastAPI
from router import login, user

app = FastAPI()

@app.get('/')
def home():
    return {"message":"Hi!"}

app.include_router(login.router, prefix="/login", tags=["auth"])