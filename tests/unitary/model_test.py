import json
import re
from datetime import datetime

import pytest
from bson.objectid import ObjectId
from pydantic_core._pydantic_core import ValidationError

from app.models.base import SystemBaseModel
from app.models.registers import RegisterBaseModel, RegisterModel


class TestBaseModel:
    def test_system_base_model(self):
        doc = SystemBaseModel(user_id=str(ObjectId())).model_dump(by_alias=True)
        assert isinstance(doc["_id"], ObjectId)
        assert isinstance(doc["user_id"], ObjectId)
        assert isinstance(doc["created_at"], datetime)
        assert isinstance(doc["updated_at"], datetime)

    def test_fields_as_json(self):
        doc = json.loads(
            SystemBaseModel(
                user_id=ObjectId("653ba8b2c9d01c3b755935ca")
            ).model_dump_json()
        )
        assert doc["user_id"] == "653ba8b2c9d01c3b755935ca"
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
            amount=100.0,
        ).model_dump(by_alias=True)

        del register["_id"]
        del register["updated_at"]
        del register["created_at"]

        assert register == {
            "amount": 100.0,
            "category": "category",
            "description": "description",
            "isPercentage": False,
            "isRequired": True,
            "isPaid": False,
            "percentage": None,
            "percentageOn": None,
            "user_id": ObjectId("653ba8b2c9d01c3b755935ca"),
        }


class TestAmountRegisterModel:
    def test_amount_register_model(self):
        register = RegisterBaseModel(
            description="description",
            category="category",
            isPercentage=False,
            isRequired=True,
            isPaid=False,
            amount=100.0,
            percentage=0.5,
            percentageOn=[{"_id": ObjectId(), "category": "categ", "amount": 100}],
        ).model_dump(by_alias=True)
        assert register == {
            "description": "description",
            "category": "category",
            "isPercentage": False,
            "isRequired": True,
            "isPaid": False,
            "amount": 100.0,
            "percentage": None,
            "percentageOn": None,
        }

    def test_amount_register_without_amount_field(self):
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
            amount=100.0,
            percentage=0.5,
            percentageOn=[
                {
                    "_id": ObjectId("653ba8b2c9d01c3b755935ca"),
                    "category": "categ",
                    "amount": 100,
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
                    "amount": 100.0,
                }
            ],
            "amount": None,
        }

    def test_percentage_register_without_amount_field(self):
        with pytest.raises(ValidationError):
            RegisterBaseModel(
                description="description",
                category="category",
                isPercentage=True,
                isRequired=True,
            )
