import json

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.core import auth
from app.routers.auth.module import (create_user,
                                     get_current_user_by_google_login)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=["auth"])


@router.post("/google_login")
def google_login(data: dict):
    current_user = get_current_user_by_google_login(data["credential"])
    if not current_user:
        id_info = auth.decode_google_token(data["credential"])
        current_user = create_user(
            name=id_info["name"],
            email=id_info["email"],
            password=None,
            google_sub=id_info["sub"],
        )

    return {
        "token": auth.create_user_access_token(current_user.email),
        "user": json.loads(
            current_user.model_dump_json(by_alias=True, exclude={"password"})
        ),
    }
