from datetime import datetime
from typing import Annotated, Any

from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

REGEX_ISODATE = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"


class ObjectIdAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v

        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, _handler
    ) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class SystemBaseModel(BaseModel):
    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}

    id: Annotated[
        ObjectId,
        ObjectIdAnnotation,
        Field(
            default_factory=ObjectId, alias="_id", examples=["6526b0e5b30dbe90dcd63192"]
        ),
    ]
    created_at: datetime = Field(
        default_factory=datetime.now, examples=["2000-01-01 00:00:00"]
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, examples=["2000-01-01 00:00:00"]
    )
