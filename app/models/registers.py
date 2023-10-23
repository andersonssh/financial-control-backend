from datetime import datetime
from typing import Annotated, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, confloat

from app.models.base import ObjectIdAnnotation


class RegisterModel(BaseModel):
    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}

    id: Annotated[
        ObjectId,
        ObjectIdAnnotation,
        Field(alias="_id", examples=["6526b0e5b30dbe90dcd63192"]),
    ]
    user_id: Annotated[
        ObjectId,
        ObjectIdAnnotation,
        Field(examples=["6526b0e5b30dbe90dcd63192"]),
    ]
    created_at: datetime = Field(examples=["2000-01-01 00:00:00"])
    description: str = None
    category: str = None
    isPercentage: bool = None
    isRequired: bool = None
    percentage: confloat(ge=0, le=1) = None
    percentageOn: List[Annotated[ObjectId, ObjectIdAnnotation]] = Field(
        None, examples=[["65354001a527d6e17d857228"]]
    )
    amount: float = None


class GetRegisters(BaseModel):
    data: List[RegisterModel]


class PostRegister(BaseModel):
    category: str
    description: str
    isPercentage: bool
    isRequired: bool
    percentage: confloat(ge=0, le=1) = None
    percentageOn: List[
        Annotated[
            ObjectId,
            ObjectIdAnnotation,
            Field(examples=[["65354001a527d6e17d857228"]]),
        ]
    ]
    amount: float = None


class PatchRegister(BaseModel):
    category: str = None
    description: str = None
    isPercentage: bool = None
    isRequired: bool = None
    percentage: confloat(gt=0, lt=1) = None
    percentageOn: List[Annotated[ObjectId, ObjectIdAnnotation]] = Field(
        examples=[["65354001a527d6e17d857228"]]
    )
    amount: float = None
