import os

from jose import jwt

from app.core import database


class TestGoogleLogin:
    def test_google_login(self, client, user):
        database.insert_one("users", user)
        response = client.post(
            "/google_login",
            json={
                "credential": jwt.encode(
                    {"email": "user@email.com"},
                    os.environ["GOOGLE_PUBLIC_KEY"],
                )
            },
        )
        assert response.status_code == 200
        assert "token" in response.json()
        token = response.json()["token"]
        decoded_token = jwt.decode(token, os.environ["SECRET_KEY"])
        assert "email" in decoded_token
        assert decoded_token["email"] == "user@email.com"

    def test_google_login_new_user(self, client):
        response = client.post(
            "/google_login",
            json={
                "credential": jwt.encode(
                    {"email": "user@email.com", "name": "User Name"},
                    os.environ["GOOGLE_PUBLIC_KEY"],
                )
            },
        )
        assert response.status_code == 200
        assert "token" in response.json()
        token = response.json()["token"]
        decoded_token = jwt.decode(token, os.environ["SECRET_KEY"])
        assert "email" in decoded_token
        assert decoded_token["email"] == "user@email.com"

        db_user = database.find_one("users", {"email": decoded_token["email"]})
        del db_user["created_at"]
        del db_user["updated_at"]
        assert db_user == {
            "_id": db_user["_id"],
            "name": "User Name",
            "email": decoded_token["email"],
            "password": None,
        }
