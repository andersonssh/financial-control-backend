import json
import re
from datetime import datetime

import pytest
from bson.objectid import ObjectId
from pydantic_core._pydantic_core import ValidationError

from app.models.auth_model import GoogleLoginModel
from app.models.base import SystemBaseModel
from app.models.registers import RegisterBaseModel, RegisterModel
from app.models.users import Users


class TestBaseModel:
    def test_system_base_model(self):
        doc = SystemBaseModel().model_dump(by_alias=True)
        assert isinstance(doc["_id"], ObjectId)
        assert isinstance(doc["created_at"], datetime)
        assert isinstance(doc["updated_at"], datetime)

    def test_fields_as_json(self):
        doc = json.loads(SystemBaseModel().model_dump_json())
        assert re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", doc["created_at"])
        assert re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", doc["updated_at"])


class TestRegisterFullModel:
    def test_register_full_model(self):
        register = RegisterModel(
            user_id=ObjectId("653ba8b2c9d01c3b755935ca"),
            description="description",
            category="category",
            isPercentage=False,
            isRequired=True,
            isPaid=False,
            value=100.0,
        ).model_dump(by_alias=True)

        del register["_id"]
        del register["updated_at"]
        del register["created_at"]

        assert register == {
            "value": 100.0,
            "category": "category",
            "description": "description",
            "isPercentage": False,
            "isRequired": True,
            "isPaid": False,
            "percentage": None,
            "percentageOn": None,
            "user_id": ObjectId("653ba8b2c9d01c3b755935ca"),
        }


class TestRegisterModel:
    def test_register_model(self):
        register = RegisterBaseModel(
            description="description",
            category="category",
            isPercentage=False,
            isRequired=True,
            isPaid=False,
            value=100.0,
            percentage=0.5,
            percentageOn=[{"_id": ObjectId(), "category": "categ", "value": 100}],
        ).model_dump(by_alias=True)
        assert register == {
            "description": "description",
            "category": "category",
            "isPercentage": False,
            "isRequired": True,
            "isPaid": False,
            "value": 100.0,
            "percentage": None,
            "percentageOn": None,
        }

    def test_register_without_value_field(self):
        with pytest.raises(ValidationError):
            RegisterBaseModel(
                description="description",
                category="category",
                isPercentage=False,
                isRequired=True,
            )


class TestPercentageRegisterModel:
    def test_percentage_register_model(self):
        register = RegisterBaseModel(
            description="description",
            category="category",
            isPercentage=True,
            isRequired=True,
            isPaid=False,
            value=100.0,
            percentage=0.5,
            percentageOn=[
                {
                    "_id": ObjectId("653ba8b2c9d01c3b755935ca"),
                    "category": "categ",
                    "value": 100,
                }
            ],
        ).model_dump(by_alias=True)
        assert register == {
            "description": "description",
            "category": "category",
            "isPercentage": True,
            "isRequired": True,
            "isPaid": False,
            "percentage": 0.5,
            "percentageOn": [
                {
                    "_id": ObjectId("653ba8b2c9d01c3b755935ca"),
                    "category": "categ",
                    "value": 100.0,
                }
            ],
            "value": None,
        }

    def test_percentage_register_without_value_field(self):
        with pytest.raises(ValidationError):
            RegisterBaseModel(
                description="description",
                category="category",
                isPercentage=True,
                isRequired=True,
            )


class TestGoogleLoginModel:
    def test_google_login_model(self):
        google_login = GoogleLoginModel(
            credential="credential",
        ).model_dump()
        assert google_login == {"credential": "credential"}


class TestUserModel:
    def test_user_model(self):
        user = Users(
            name="name  ",
            email="email@email.com",
            password="password",
            google_sub="xxx",
        ).model_dump(by_alias=True)

        created_at = user.pop("created_at")
        updated_at = user.pop("updated_at")
        assert isinstance(created_at, datetime)
        assert isinstance(updated_at, datetime)
        assert user == {
            "_id": user["_id"],
            "name": "name",
            "email": "email@email.com",
            "password": "password",
            "google_sub": "xxx",
        }
