from typing import Annotated, Any, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, confloat, model_validator

from app.models.base import ObjectIdAnnotation, SystemBaseModel


class AmountRegisterEmbeddedModel(BaseModel):
    id: Annotated[
        ObjectId,
        ObjectIdAnnotation,
        Field(alias="_id", examples=["6526b0e5b30dbe90dcd63192"]),
    ]
    category: str
    amount: float


class RegisterBaseModel(BaseModel):
    description: str
    category: str
    isPercentage: bool
    isRequired: bool
    amount: float | None = None
    percentageOn: List[AmountRegisterEmbeddedModel] | None = None
    percentage: confloat(ge=0, le=1) | None = None

    @model_validator(mode="before")
    @classmethod
    def required_fields(cls, data: Any):
        if data["isPercentage"]:
            assert (
                data.get("percentage") is not None
            ), 'when isPercentage=true "percentage" must be set'
            data["amount"] = None
        else:
            assert (
                data.get("amount") is not None
            ), 'when isPercentage=false "amount" must be set'
            data["percentageOn"] = None
            data["percentage"] = None
        return data


class RegisterModel(RegisterBaseModel, SystemBaseModel):
    pass


class GetRegistersModel(BaseModel):
    data: List[RegisterModel]
