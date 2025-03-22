from typing import Annotated, Any, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, confloat, model_validator

from app.models.base import ObjectIdAnnotation, SystemBaseModel


class RegisterEmbeddedModel(BaseModel):
    id: Annotated[
        ObjectId,
        ObjectIdAnnotation,
        Field(alias="_id", examples=["6526b0e5b30dbe90dcd63192"]),
    ]
    category: str
    value: float


class RegisterBaseModel(BaseModel):
    description: str
    category: str
    isRequired: bool
    isHidden: bool = False
    value: float | None = None
    isPaid: bool = None


class RegisterModel(RegisterBaseModel, SystemBaseModel):
    user_id: Annotated[
        ObjectId,
        ObjectIdAnnotation,
        Field(examples=["6526b0e5b30dbe90dcd63192"]),
    ]


class GetRegistersModel(BaseModel):
    data: List[RegisterModel]


class PatchRegisterModel(BaseModel):
    description: str = None
    category: str = None
    isPaid: bool = None
