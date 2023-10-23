import datetime
from unittest.mock import patch

import mongomock
import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def patch_db():
    mock_db = mongomock.MongoClient().db
    with patch("app.database.db", mock_db):
        yield mock_db


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def current_user():
    return {
        "_id": ObjectId("6526b0e5b30dbe90dcd63192"),
        "name": "Current User",
        "email": "currentuser@email.com.br",
    }


@pytest.fixture()
def register():
    return {
        "_id": ObjectId("653587ab79609ae20beb9559"),
        "user_id": ObjectId("6526b0e5b30dbe90dcd63192"),
        "created_at": datetime.datetime.fromisoformat("2000-01-01 00:00:00"),
        "description": "streaming",
        "category": "entertainment",
        "isPercentage": False,
        "isRequired": True,
        "percentage": 0,
        "percentageOn": [ObjectId("65354001a527d6e17d857228")],
        "amount": 100,
    }
