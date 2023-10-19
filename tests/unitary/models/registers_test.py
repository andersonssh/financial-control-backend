from datetime import datetime

from bson.objectid import ObjectId

from app.models.registers import RegisterModel, GetRegisters


class TestRegisterModel:
    def test_register_model(self):
        assert RegisterModel(
            _id=ObjectId("65309236cc11b109bbe4b0d5"),
            user_id=ObjectId("65309236cc11b109bbe4b0d6"),
            created_at=datetime.fromisoformat("2001-01-01 01:01:01"),
            title="title",
            description="description",
            category="category",
            isPercentage=True,
            isRequired=True,
            percentage=0.5,
            percentageOn=[ObjectId("65309236cc11b109bbe4b0d7")],
            amount=100.0,
        ).model_dump() == {
            "id": "65309236cc11b109bbe4b0d5",
            "user_id": "65309236cc11b109bbe4b0d6",
            "created_at": "2001-01-01 01:01:01",
            "title": "title",
            "description": "description",
            "category": "category",
            "isPercentage": True,
            "isRequired": True,
            "percentage": 0.5,
            "percentageOn": ["65309236cc11b109bbe4b0d7"],
            "amount": 100.0,
        }

    def test_get_register_model(self):
        assert GetRegisters(
            data=[
                RegisterModel(
                    _id=ObjectId("65309236cc11b109bbe4b0d5"),
                    user_id=ObjectId("65309236cc11b109bbe4b0d6"),
                    created_at=datetime.fromisoformat("2001-01-01 01:01:01"),
                )
            ]
        ).model_dump(exclude_unset=True) == {
            "data": [
                {
                    "id": "65309236cc11b109bbe4b0d5",
                    "user_id": "65309236cc11b109bbe4b0d6",
                    "created_at": "2001-01-01 01:01:01",
                }
            ]
        }
