from typing import Annotated
from .database import get_db, Database
from fastapi import Depends

GetDB = Annotated[Database, Depends(get_db)]