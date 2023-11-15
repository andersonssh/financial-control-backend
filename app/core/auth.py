import os
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = os.environ["SECRET_KEY"]

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


def create_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_token(token: str, google_token: bool = False) -> dict:
    secret_key = os.environ["GOOGLE_PUBLIC_KEY"] if google_token else SECRET_KEY
    return jwt.decode(
        token,
        secret_key,
        audience=os.environ["GOOGLE_CLIENT_ID"] if google_token else None,
    )
