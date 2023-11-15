from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.core import auth

from .auth_module import create_user, get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=["auth"])


@router.post("/google_login")
def google_login(data: dict):
    current_user = get_current_user(data["credential"], True)
    if not current_user:
        payload = auth.decode_token(data["credential"], True)
        current_user = create_user(
            name=payload.get("name"), email=payload.get("email"), password=None
        )

    return {"token": auth.create_user_access_token(current_user.email)}
