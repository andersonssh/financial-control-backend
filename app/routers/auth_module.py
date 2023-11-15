from fastapi import HTTPException, status
from jose.exceptions import JWTError

from app.core import auth, database
from app.models.users import Users as User


def get_current_user(token: str, google_token: bool = False) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.decode_token(token, google_token=google_token)
        if not payload.get("email"):
            raise credentials_exception
        email = payload["email"]
    except JWTError:
        raise credentials_exception
    user = database.find_one("users", {"email": email})
    if not user:
        return None
    return User(**user)


def create_user(name: str, email: str, password: str | None) -> User:
    user = User(
        name=name,
        email=email,
        password=auth.get_password_hash(password) if password else None,
    )
    database.insert_one("users", user.model_dump(by_alias=True))
    return user
