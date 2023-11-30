import os
from unittest.mock import patch

from jose import jwt

from app.core import database


class TestGoogleLogin:
    @patch(
        "app.core.auth.decode_google_token",
        lambda __: {
            "email": "user@email.com",
            "iss": "accounts.google.com",
            "name": "ex ex",
            "sub": "id",
        },
    )
    def test_google_login(self, client, user):
        database.insert_one("users", user)
        response = client.post(
            "/google_login",
            json={"credential": {}},
        )
        assert response.status_code == 200
        assert "token" in response.json()
        token = response.json()["token"]
        decoded_token = jwt.decode(token, os.environ["SECRET_KEY"])
        assert "email" in decoded_token
        assert decoded_token["email"] == "user@email.com"
        user_response = response.json()["user"]
        assert user_response["name"] == "ex ex"
        assert user_response["email"] == "user@email.com"

    @patch(
        "app.core.auth.decode_google_token",
        lambda __: {
            "email": "user@email.com",
            "iss": "accounts.google.com",
            "name": "User Name",
            "sub": "id",
        },
    )
    def test_google_login_new_user(self, client):
        response = client.post(
            "/google_login",
            json={"credential": {}},
        )
        assert response.status_code == 200
        assert "token" in response.json()
        token = response.json()["token"]
        user = response.json()["user"]
        assert user["name"] == "User Name"
        assert user["email"] == "user@email.com"
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
            "google_sub": "id",
        }
