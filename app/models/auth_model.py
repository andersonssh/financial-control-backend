from pydantic import BaseModel


class GoogleLoginModel(BaseModel):
    credential: str
