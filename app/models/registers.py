from typing import Annotated, Any, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, confloat

from app.models.base import ObjectIdAnnotation, SystemBaseModel


class _RegisterBase:
    description: str
    category: str
    isRequired: bool


class _AmountRegisterBase:
    amount: float


class _AmountRegisterEmbeddedModel(BaseModel):
    id: Annotated[
        ObjectId,
        ObjectIdAnnotation,
        Field(alias="_id", examples=["6526b0e5b30dbe90dcd63192"]),
    ]
    category: str
    amount: float


class _PercentageRegisterBase(BaseModel):
    percentageOn: List[_AmountRegisterEmbeddedModel] = None
    percentage: confloat(ge=0, le=1)


class RegisterModel(_RegisterBase, SystemBaseModel):
    pass


class AmountRegisterModel(_AmountRegisterBase, RegisterModel):
    pass


class PercentageRegisterModel(_PercentageRegisterBase, RegisterModel):
    pass


class GetRegistersModel(BaseModel):
    data: List[PercentageRegisterModel | AmountRegisterModel]


class PostPutAmountRegisterModel(BaseModel, _AmountRegisterBase):
    pass


class PostPutPercentageRegisterModel(_PercentageRegisterBase, BaseModel):
    pass


if __name__ == "__main__":
    print(
        PostPutPercentageRegisterModel(
            **{
                "_id": "6526b0e5b30dbe90dcd63192",
                "user_id": "6526b0e5b30dbe90dcd63192",
                "created_at": "2000-01-01 00:00:00",
                "description": "string",
                "category": "string",
                "isRequired": True,
                "percentageOn": [
                    {"_id": "6526b0e5b30dbe90dcd63192", "category": "oi", "amount": 0}
                ],
                "percentage": 1,
                "amount": 0,
            }
        ).model_dump_json(by_alias=True)
    )
