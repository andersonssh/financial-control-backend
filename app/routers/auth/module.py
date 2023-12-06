
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
    database.insert_one("users", user.model_dump(by_alias=True, exclude_none=True))
    return user


if __name__ == "__main__":
    id_info = id_token.verify_oauth2_token(
        "eyJhbGciOiJSUzI1NiIsImtpZCI6IjBlNzJkYTFkZjUwMWNhNmY3NTZiZjEwM2ZkN2M3MjAyOTQ3NzI1MDYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5MDEzMjM0OTAxODUtYTg4OTFnYXRxM3VnbDNobDRlcTNxZ245dWtpYTJsdWUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5MDEzMjM0OTAxODUtYTg4OTFnYXRxM3VnbDNobDRlcTNxZ245dWtpYTJsdWUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDgwNjI0NzczMDIwMDkzMTA1ODgiLCJlbWFpbCI6ImFuZGVyc29uZGV2LnNzaEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmJmIjoxNzAxMzU1NTE3LCJuYW1lIjoiYW5kZXJzb24gZGV2IiwiZ2l2ZW5fbmFtZSI6ImFuZGVyc29uIiwiZmFtaWx5X25hbWUiOiJkZXYiLCJsb2NhbGUiOiJwdC1CUiIsImlhdCI6MTcwMTM1NTgxNywiZXhwIjoxNzAxMzU5NDE3LCJqdGkiOiI5ZDE4ZmIwYTIyOTI5NDc0YzQ2ZjYwNDQwOGU0ZjdmYWYzYWVjODEzIn0.GyFzHQU1ZrZ6YmxX8DOKskQCx7sMCZt14Lc3iaYk_qBZvrVllh7kM7nHBkpabeId9pchtwZlycNfJsPhjxppxQo5a8nV49UqSC0QgErRTzrMEL6eB7bUbCoMaas3nkzdwTfmbNCEu8tbVGBHY29GTL4006iCD2ftjvqaP9qmS97AU1KoUL-FY-RZozPv4q1Wul0Xr59e6z2pAmDI2nmm-bRpm-56KWxU4ueScYs75YPJjDC4Az9eZn-FyXn4xkpd8UUsmJGGnpBkNg95PTX7VEEQ2dTtMveOJcE6U3cxNF808ff9oEx6lOUqhoNyqE2eY-2Yh8JtXHYnM1qmZgjR2A",
        requests.Request(),
        "901323490185-a8891gatq3ugl3hl4eq3qgn9ukia2lue.apps.googleusercontent.com",
    )
    print(id_info)
