import os
from datetime import datetime, timedelta

from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_access_token(user_email: str, expires_delta: timedelta = None) -> str:
    to_encode = {"email": user_email}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=300))
    to_encode["exp"] = expire
    return create_token(to_encode)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def get_password_hash(raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def decode_google_token(token: str) -> dict:
    return id_token.verify_oauth2_token(
        token, requests.Request(), os.environ["GOOGLE_CLIENT_ID"]
    )


def create_token(data: dict) -> str:
    return jwt.encode(data, os.environ["SECRET_KEY"], algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, os.environ["SECRET_KEY"])
