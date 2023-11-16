import os
from datetime import datetime

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient
from jose import jwt

from app.core import database
from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def current_user():
    current_user = {
        "_id": ObjectId("6526b0e5b30dbe90dcd63192"),
        "name": "Current User",
        "email": "currentuser@email.com.br",
        "created_at": datetime(2001, 1, 1, 0, 0, 0),
        "updated_at": datetime(2001, 1, 1, 0, 0, 0),
        "password": None,
    }
    database.insert_one("users", current_user)
    return current_user


@pytest.fixture()
def auth_headers():
    token = jwt.encode(
        {"email": "currentuser@email.com.br"},
        os.environ["SECRET_KEY"],
    )
    return {"Authorization": f"Bearer {token}"}
