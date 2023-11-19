from . import schemas
from . import auth

# Sanitizers
'''
Sanitizers should secure that all data that goes to CRUD functions follows the correct patterns
'''

def new_user_sanitisation(user: schemas.UserCreate):
    user = schemas.UserInDB(**user.model_dump())
    user.password = auth.get_password_hash(user.password)
    return user