from pydantic import BaseModel


class GoogleLoginModel(BaseModel):
    credential: str


class GoogleLoginResponseModel(BaseModel):
    token: str
    user: dict
