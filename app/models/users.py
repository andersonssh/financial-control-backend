from pydantic import EmailStr, constr

from app.models.base import SystemBaseModel


class Users(SystemBaseModel):
    name: constr(strip_whitespace=True)
    email: EmailStr
    password: str | None
    google_sub: str | None = None
