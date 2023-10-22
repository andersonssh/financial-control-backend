from typing import List

from pydantic import Field, confloat

from app.models.base import CustomDatetime, CustomModel, PyObjectId


class RegisterModel(CustomModel):
    id: PyObjectId = Field(None, alias="_id")
    user_id: PyObjectId = Field(examples=["65354001a527d6e17d857228"])
    created_at: CustomDatetime = Field(examples=["2000-01-01 00:00:00"])
    title: str = None
    description: str = None
    category: str = None
    isPercentage: bool = None
    isRequired: bool = None
    percentage: confloat(ge=0, le=1) = None
    percentageOn: List[PyObjectId] = Field(None, examples=["65354001a527d6e17d857228"])
    amount: float = None


class PostRegister(CustomModel):
    category: str
    description: str
    isPercentage: bool
    isRequired: bool
    title: str
    percentage: confloat(ge=0, le=1) = None
    percentageOn: List[PyObjectId] = Field(None, examples=[["65354001a527d6e17d857228"]])
    amount: float = None


class GetRegisters(CustomModel):
    data: List[RegisterModel]


class PatchRegister(CustomModel):
    category: str = None
    title: str = None
    description: str = None
    isPercentage: bool = None
    isRequired: bool = None
    percentage: confloat(gt=0, lt=1) = None
    percentageOn: List[PyObjectId] = Field(None, examples=[["65354001a527d6e17d857228"]])
    amount: float = None
