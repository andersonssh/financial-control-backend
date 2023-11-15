import os
from datetime import datetime
from unittest.mock import patch

import mongomock
import pytest
from bson.objectid import ObjectId

os.environ["SECRET_KEY"] = "secret_key"
os.environ["GOOGLE_PUBLIC_KEY"] = "google_public_key"
os.environ["GOOGLE_CLIENT_ID"] = "google_client_id"


@pytest.fixture(autouse=True)
def patch_db():
    mock_db = mongomock.MongoClient().db
    with patch("app.core.database.db", mock_db):
        yield mock_db


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


@pytest.fixture()
def user():
    return {
        "_id": ObjectId("653587ab79609ae20beb9560"),
        "created_at": datetime(2001, 1, 1, 0, 0, 0),
        "updated_at": datetime(2001, 1, 1, 0, 0, 0),
        "name": "user",
        "email": "user@email.com",
        "password": None,
    }
