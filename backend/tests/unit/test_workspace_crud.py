from fastapi import HTTPException
import pytest

from app import schemas, auth
from tests.unit.default_db import close_db, dbs


global_id = ''


# GET
# def test_get_all():
#     workspaces = dbs.workspaces.get_all()