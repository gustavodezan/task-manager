from app.dependencies import GetDBs
from app.database import get_db

def get_dbs(a):
    # print(a)
    return GetDBs(next(get_db()))

dbs = GetDBs(next(get_db()))