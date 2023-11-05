from datetime import datetime
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
        "created_at": datetime(2001, 1, 1, 0, 0, 0),
        "updated_at": datetime(2001, 1, 1, 0, 0, 0),
        "description": "streaming",
        "category": "entertainment",
        "isPercentage": False,
        "isRequired": True,
        "isPaid": False,
        "value": 100,
    }


@pytest.fixture()
def percentage_register():
    return {
        "_id": ObjectId("653587ab79609ae20beb9560"),
        "user_id": ObjectId("6526b0e5b30dbe90dcd63192"),
        "created_at": datetime(2001, 1, 1, 0, 0, 0),
        "updated_at": datetime(2001, 1, 1, 0, 0, 0),
        "description": "streaming",
        "category": "entertainment",
        "isPercentage": True,
        "isRequired": True,
        "isPaid": False,
        "percentage": 0,
        "percentageOn": [
            {
                "_id": ObjectId("653ba8b2c9d01c3b755935ca"),
                "category": "category",
                "value": 100,
            }
        ],
    }
