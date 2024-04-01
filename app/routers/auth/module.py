
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.auth.transport import requests
from google.oauth2 import id_token
from jose.exceptions import JWTError

from app.core import auth, database
from app.models.users import Users as User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user_by_google_login(token: str) -> User | None:
    id_info = auth.decode_google_token(token)
    if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong issuer",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = database.find_one("users", {"google_sub": id_info["sub"]})
    if not db_user:
        return None

    return User(**db_user)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.decode_token(token)
        if not payload.get("email"):
            raise credentials_exception
        email = payload["email"]
    except JWTError:
        raise credentials_exception
    user = database.find_one("users", {"email": email})
    if not user:
        return None
    return User(**user)


def create_user(
    name: str, email: str, password: str | None, google_sub: str | None = None
) -> User:
    user = User(
        name=name,
        email=email,
        password=auth.get_password_hash(password) if password else None,
        google_sub=google_sub,
    )
    database.insert_one("users", user.model_dump(by_alias=True))
    return user
