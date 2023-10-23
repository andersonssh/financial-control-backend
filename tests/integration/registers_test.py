from app import database


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
