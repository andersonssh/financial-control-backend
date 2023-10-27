import json
import re
from datetime import datetime

from bson.objectid import ObjectId

from app.models.base import SystemBaseModel
from app.models.registers import AmountRegisterModel, PercentageRegisterModel


class TestBaseModel:
    def test_system_base_model(self):
        doc = SystemBaseModel(user_id=str(ObjectId())).model_dump(by_alias=True)
        assert isinstance(doc["_id"], ObjectId)
        assert isinstance(doc["user_id"], ObjectId)
        assert isinstance(doc["created_at"], datetime)
        assert isinstance(doc["updated_at"], datetime)

    def test_datetime_fields_as_json(self):
        doc = json.loads(SystemBaseModel(user_id=ObjectId()).model_dump_json())
        assert re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", doc["created_at"])
        assert re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", doc["updated_at"])


class TestAmountRegisterModel:
    def test_amount_register_model(self):
        register = AmountRegisterModel(
            user_id=ObjectId("65309236cc11b109bbe4b0d6"),
            description="description",
            category="category",
            isPercentage=True,
            isRequired=True,
            percentage=0.5,
            amount=100.0,
        )
        register = register.model_dump(by_alias=True)
        del register["created_at"]
        del register["updated_at"]
        del register["_id"]
        del register["user_id"]
        assert register == {
            "description": "description",
            "category": "category",
            "isRequired": True,
            "amount": 100.0,
        }

    def test_percentage_register_model(self):
        register = PercentageRegisterModel(
            user_id=ObjectId("65309236cc11b109bbe4b0d6"),
            description="description",
            category="category",
            isPercentage=True,
            isRequired=True,
            percentageOn=[
                {
                    "_id": ObjectId("65309236cc11b109bbe4b0d6"),
                    "category": "embedded document category",
                    "amount": 10,
                }
            ],
            percentage=0.5,
            amount=100.0,
        )
        register = register.model_dump(by_alias=True)
        del register["created_at"]
        del register["updated_at"]
        del register["_id"]
        del register["user_id"]
        assert register == {
            "description": "description",
            "category": "category",
            "isRequired": True,
            "percentage": 0.5,
            "percentageOn": [
                {
                    "_id": ObjectId("65309236cc11b109bbe4b0d6"),
                    "category": "embedded document category",
                    "amount": 10.0,
                }
            ]
        }
