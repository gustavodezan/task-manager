# from datetime import datetime, timedelta

# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm

# from app import auth, crud
# from app.schemas import Token, User, UserInDB
# from utils.encryption import encrypt_user, decrypt

# import os
# from pathlib import Path
# from dotenv import load_dotenv

# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path=env_path)

# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# router = APIRouter()

# @router.post('/register', response_model=User)
# async def register(user: UserInDB):
#     """Create user from CRM request"""
#     users = crud.User.get_users_raw()
#     for u in users:
#         if decrypt(u["email"].encode('utf-8')) == user.email:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken")
#     user.password = auth.get_password_hash(user.password)
#     data = encrypt_user(user.dict())
#     return crud.User.create(data)


# @router.post("/", response_model=Token)
# async def login_for_acess_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = auth.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
#     for scope in form_data.scopes:
#         if scope not in user.scopes:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, detail="You do not have the requested permissions"
#             )

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = auth.create_access_token(
#         data={"sub": user.email, "scopes": form_data.scopes},
#         expires_delta=access_token_expires
#     )
    
#     return {"access_token": access_token, "token_type": "bearer", "expire": ACCESS_TOKEN_EXPIRE_MINUTES}
