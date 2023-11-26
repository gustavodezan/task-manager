from datetime import timedelta

from fastapi import APIRouter
from fastapi import FastAPI, Depends, status, HTTPException, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from .. import crud, schemas
from .. import auth
from ..dependencies import UserDB
from ..constants import ACCESS_TOKEN_EXPIRE_TIME


router = APIRouter()


@router.post('/login', response_model=schemas.Token)
def login(db: UserDB, form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    access_token = auth.create_access_token({"sub": user.email, "scopes": form_data.scopes}, access_token_expires)
    return schemas.Token(access_token=access_token, token_type="bearer", expire=ACCESS_TOKEN_EXPIRE_TIME)