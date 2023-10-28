import copy
import re
from datetime import datetime

from bson.objectid import ObjectId

from app import database

# TODO: faqzer teste que muda tipo de amount para percentage documento ja salvo no banco


class TestGetRegisters:
    def test_get_registers(
        self, client, current_user, amount_register, percentage_register
    ):
        database.insert_one("registers", amount_register)
        database.insert_one("registers", percentage_register)

        response = client.get("/registers")
        assert response.status_code == 200
        assert response.json() == {
            "data": [
                {
                    "_id": "653587ab79609ae20beb9559",
                    "amount": 100.0,
                    "category": "entertainment",
                    "created_at": "2001-01-01 00:00:00",
                    "description": "streaming",
                    "isPercentage": False,
                    "isRequired": True,
                    "updated_at": "2001-01-01 00:00:00",
                    "user_id": "6526b0e5b30dbe90dcd63192",
                },
                {
                    "_id": "653587ab79609ae20beb9560",
                    "category": "entertainment",
                    "created_at": "2001-01-01 00:00:00",
                    "description": "streaming",
                    "isPercentage": True,
                    "isRequired": True,
                    "percentage": 0.0,
                    "percentageOn": [
                        {
                            "_id": "653ba8b2c9d01c3b755935ca",
                            "amount": 100.0,
                            "category": "category",
                        }
                    ],
                    "updated_at": "2001-01-01 00:00:00",
                    "user_id": "6526b0e5b30dbe90dcd63192",
                },
            ]
        }

    def test_get_only_user_registers(self, client, current_user, amount_register):
        database.insert_one("registers", amount_register)
        amount_register["_id"] = ObjectId()
        amount_register["user_id"] = ObjectId()
        database.insert_one("registers", amount_register)
        response = client.get("/registers")
        assert response.status_code == 200

        returned_registers = response.json()["data"]
        assert len(returned_registers) == 1
        assert returned_registers[0]["user_id"] == str(current_user["_id"])


class TestPostRegister:
    amount_register_payload = {
        "category": "string",
        "description": "string",
        "isPercentage": False,
        "isRequired": False,
        "amount": 0,
    }
    percentage_register_payload = {
        "category": "string",
        "description": "string",
        "isPercentage": True,
        "isRequired": False,
        "percentage": 1,
        "percentageOn": [
            {
                "_id": ObjectId("653ba8b2c9d01c3b755935ca"),
                "category": "categ",
                "amount": 100,
            }
        ],
    }

    def test_post_register(self, client, current_user):
        response = client.post("/registers", json=self.amount_register_payload)
        assert response.status_code == 201

        returned_register = response.json()
        expected_register = copy.deepcopy(self.amount_register_payload)
        expected_register["_id"] = returned_register["_id"]
        expected_register["created_at"] = returned_register["created_at"]
        expected_register["updated_at"] = returned_register["updated_at"]
        expected_register["user_id"] = str(current_user["_id"])
        assert returned_register == expected_register

    def test_saved_db_register(self, client, current_user):
        response = client.post("/registers", json=self.amount_register_payload)
        assert response.status_code == 201
        db_register = database.find_one(
            "registers", {"_id": ObjectId(response.json()["_id"])}
        )
        assert isinstance(db_register["_id"], ObjectId)
        assert isinstance(db_register["user_id"], ObjectId)
        assert isinstance(db_register["created_at"], datetime)
        assert isinstance(db_register["updated_at"], datetime)
        assert isinstance(db_register["isPercentage"], bool)
        assert isinstance(db_register["isRequired"], bool)
        assert isinstance(db_register["amount"], float)
        assert isinstance(db_register["description"], str)
        assert isinstance(db_register["category"], str)
        assert db_register["percentage"] is None
        assert db_register["percentageOn"] is None


# class TestPutRegister:
#     def test_put_register(self, client, current_user, amount_register):
#         amount_register.pop("percentageOn", None)
#         amount_register["description"] = "old description"
#         database.insert_one("registers", amount_register)
#         response = client.patch(
#             f"/registers/{str(amount_register['_id'])}",
#             json={"category": "new category", "percentageOn": [str(ObjectId())]},
#         )
#         assert response.status_code == 204
#         db_register = database.find_one("registers", {"_id": amount_register["_id"]})
#         assert db_register["category"] == "new category"
#         assert db_register["description"] == "old description"
#         assert isinstance(db_register["percentageOn"][0], ObjectId)
#
#     def test_edit_other_user_register(self, client, current_user, register):
#         register["user_id"] = ObjectId()
#         database.insert_one("registers", register)
#         response = client.patch(
#             f"/registers/{str(register['_id'])}", json={"category": "new category"}
#         )
#         assert response.status_code == 404
#         db_register = database.find_one("registers", {"_id": register["_id"]})
#         assert db_register["category"] != "new category"


class TestDeleteRegister:
    def test_delete_register(self, client, current_user, amount_register):
        database.insert_one("registers", amount_register)
        response = client.delete(f"/registers/{str(amount_register['_id'])}")
        assert response.status_code == 204
        assert not database.find_one("registers", {"_id": amount_register["_id"]})

    def test_delete_other_user_register(self, client, current_user, amount_register):
        amount_register["user_id"] = ObjectId()
        database.insert_one("registers", amount_register)
        response = client.delete(f"/registers/{str(amount_register['_id'])}")
        assert response.status_code == 404
        assert database.find_one("registers", {"_id": amount_register["_id"]})
