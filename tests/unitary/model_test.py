import json
from datetime import datetime
from typing import Annotated

from bson.objectid import ObjectId

from app.models.registers import GetRegisters, RegisterModel


class TestRegisterModel:
    def test_register_model(self):
        register = RegisterModel(
            _id=ObjectId("65309236cc11b109bbe4b0d5"),
            user_id=ObjectId("65309236cc11b109bbe4b0d6"),
            created_at=datetime(2001, 1, 1, 1, 1, 1),
            description="description",
            category="category",
            isPercentage=True,
            isRequired=True,
            percentage=0.5,
            percentageOn=[ObjectId("65309236cc11b109bbe4b0d7")],
            amount=100.0,
        )
        register = json.loads(register.model_dump_json())
        assert register == {
            "id": "65309236cc11b109bbe4b0d5",
            "user_id": "65309236cc11b109bbe4b0d6",
            "created_at": "2001-01-01 01:01:01",
            "description": "description",
            "category": "category",
            "isPercentage": True,
            "isRequired": True,
            "percentage": 0.5,
            "percentageOn": ["65309236cc11b109bbe4b0d7"],
            "amount": 100.0,
        }

    def test_get_register_model(self):
        register = GetRegisters(
            data=[
                {
                    "_id": ObjectId("65309236cc11b109bbe4b0d5"),
                    "user_id": ObjectId("65309236cc11b109bbe4b0d6"),
                    "created_at": datetime(2001, 1, 1, 1, 1, 1),
                }
            ]
        )
        register = json.loads(register.model_dump_json(exclude_unset=True))
        assert register == {
            "data": [
                {
                    "id": "65309236cc11b109bbe4b0d5",
                    "user_id": "65309236cc11b109bbe4b0d6",
                    "created_at": "2001-01-01 01:01:01",
                }
            ]
        }
