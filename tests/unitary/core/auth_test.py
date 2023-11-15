import os

from jose import jwt

from app.core import auth


class TestToken:
    def test_create_user_access_token(self):
        token = auth.create_user_access_token("example@email.com")
        decoded_token = jwt.decode(token, os.environ["SECRET_KEY"])
        assert "email" in decoded_token
        assert decoded_token["email"] == "example@email.com"

    def test_create_token(self):
        token = auth.create_token({"email": "example@email.com"})
        assert token is not None
        decoded_token = jwt.decode(token, os.environ["SECRET_KEY"])
        assert "email" in decoded_token
        assert decoded_token["email"] == "example@email.com"

    def test_decode_token(self):
        token = jwt.encode({"email": "example@email.com"}, os.environ["SECRET_KEY"])
        decoded_token = auth.decode_token(token)
        assert "email" in decoded_token
        assert decoded_token["email"] == decoded_token["email"]

    def test_decode_google_token(self):
        token = jwt.encode(
            {"email": "example@email.com"}, os.environ["GOOGLE_PUBLIC_KEY"]
        )
        decoded_token = auth.decode_token(token, True)
        assert "email" in decoded_token
        assert decoded_token["email"] == decoded_token["email"]


class TestPassword:
    def test_get_password_hash(self):
        hashed_password = auth.get_password_hash("password")
        assert hashed_password is not None
        assert auth.verify_password("password", hashed_password)

    def test_verify_password(self):
        password = auth.get_password_hash("password")
        assert password is not None
        assert auth.verify_password("password", password)
        assert not auth.verify_password("wrong_password", password)
