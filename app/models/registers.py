from typing import List

from pydantic import Field, confloat

from app.models.base import CustomDatetime, CustomModel, PyObjectId


class RegisterModel(CustomModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: CustomDatetime
    title: str = None
    description: str = None
    category: str = None
    isPercentage: bool = None
    isRequired: bool = None
    percentage: confloat(gt=0, lt=1) = None
    percentageOn: List[PyObjectId] = None
    amount: float = None


class GetRegisters(CustomModel):
    data: List[RegisterModel]


#
#
# class PostRegister(BaseModel):
#     category: str
#     description: str
#     isPercentage: bool
#     isRequired: bool
#     title: str
#     percentage: confloat(gt=0, lt=1) = None
#     percentageOn: List[PyObjectId] = None
#     amount: confloat() = None
#
#
# class PatchRegister(BaseModel):
#     category: str = None
#     description: str = None
#     isPercentage: bool = None
#     isRequired: bool = None
#     percentage: confloat(gt=0, lt=1) = None
#     percentageOn: List[PyObjectId] = None
#     title: str = None
#     amount: confloat() = None


if __name__ == "__main__":
    from bson.objectid import ObjectId

    print(RegisterModel(_id=ObjectId()).model_dump(exclude_unset=True))
