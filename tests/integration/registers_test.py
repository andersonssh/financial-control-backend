from app import database
from bson.objectid import ObjectId
import copy
from datetime import datetime
import re


class TestGetRegisters:
    def test_get_registers(self, client, current_user, register):
        database.insert_one("registers", register)

        response = client.get("/registers")
        assert response.status_code == 200
        assert response.json() == {
            "data": [
                {
                    "_id": "653587ab79609ae20beb9559",
                    "user_id": "6526b0e5b30dbe90dcd63192",
                    "created_at": "2000-01-01 00:00:00",
                    "description": "streaming",
                    "category": "entertainment",
                    "isPercentage": False,
                    "isRequired": True,
                    "percentage": 0.0,
                    "percentageOn": ["65354001a527d6e17d857228"],
                    "amount": 100.0,
                }
            ]
        }

    def test_get_only_user_registers(self, client, current_user, register):
        database.insert_one("registers", register)
        register["_id"] = ObjectId()
        register["user_id"] = ObjectId()
        database.insert_one("registers", register)
        response = client.get("/registers")
        assert response.status_code == 200

        returned_registers = response.json()["data"]
        assert len(returned_registers) == 1
        assert returned_registers[0]["user_id"] == str(current_user["_id"])


class TestPostRegister:
    payload = {
        "category": "string",
        "description": "string",
        "isPercentage": False,
        "isRequired": False,
        "percentage": 1,
        "percentageOn": ["65354001a527d6e17d857228"],
        "amount": 0,
    }

    def test_post_register(self, client, current_user):
        response = client.post("/registers", json=self.payload)
        assert response.status_code == 201

        returned_register = response.json()
        expected_register = copy.deepcopy(self.payload)
        expected_register["_id"] = returned_register["_id"]
        expected_register["created_at"] = returned_register["created_at"]
        expected_register["user_id"] = str(current_user["_id"])
        assert returned_register == expected_register
        assert re.search(
            r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", returned_register["created_at"]
        )

    def test_saved_db_register(self, client, current_user):
        response = client.post("/registers", json=self.payload)
        assert response.status_code == 201
        db_register = database.find_one(
            "registers", {"_id": ObjectId(response.json()["_id"])}
        )
        assert isinstance(db_register["_id"], ObjectId)
        assert isinstance(db_register["user_id"], ObjectId)
        assert isinstance(db_register["created_at"], datetime)
        assert isinstance(db_register["percentageOn"][0], ObjectId)
        assert isinstance(db_register["isPercentage"], bool)
        assert isinstance(db_register["isRequired"], bool)
        assert isinstance(db_register["percentage"], float)
        assert isinstance(db_register["amount"], float)
        assert isinstance(db_register["description"], str)
        assert isinstance(db_register["category"], str)


class TestPatchRegister:
    def test_patch_register(self, client, current_user, register):
        register.pop("percentageOn", None)
        register["description"] = "old description"
        database.insert_one("registers", register)
        response = client.patch(
            f"/registers/{str(register['_id'])}",
            json={"category": "new category", "percentageOn": [str(ObjectId())]},
        )
        assert response.status_code == 204
        db_register = database.find_one("registers", {"_id": register["_id"]})
        assert db_register["category"] == "new category"
        assert db_register["description"] == "old description"
        assert isinstance(db_register["percentageOn"][0], ObjectId)

    def test_edit_other_user_register(self, client, current_user, register):
        register["user_id"] = ObjectId()
        database.insert_one("registers", register)
        response = client.patch(
            f"/registers/{str(register['_id'])}", json={"category": "new category"}
        )
        assert response.status_code == 404
        db_register = database.find_one("registers", {"_id": register["_id"]})
        assert db_register["category"] != "new category"


class TestDeleteRegister:
    def test_delete_register(self, client, current_user, register):
        database.insert_one("registers", register)
        response = client.delete(f"/registers/{str(register['_id'])}")
        assert response.status_code == 204
        assert not database.find_one("registers", {"_id": register["_id"]})

    def test_delete_other_user_register(self, client, current_user, register):
        register["user_id"] = ObjectId()
        database.insert_one("registers", register)
        response = client.delete(f"/registers/{str(register['_id'])}")
        assert response.status_code == 404
        assert database.find_one("registers", {"_id": register["_id"]})
