from datetime import datetime

from bson.objectid import ObjectId
from pydantic import BaseModel, ConfigDict, constr
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

REGEX_ISODATE = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"


def object_id_validate(v: ObjectId | str) -> ObjectId | str:
    assert ObjectId.is_valid(v), f"{v} is not a valid ObjectId"
    if isinstance(v, str):
        return ObjectId(v)
    return str(v)


def datetime_validate(v: datetime | str) -> datetime | str:
    if isinstance(v, str):
        return datetime.fromisoformat(v)
    return v.strftime("%Y-%m-%d %H:%M:%S")


PyObjectId = Annotated[ObjectId | str, AfterValidator(object_id_validate)]
CustomDatetime = Annotated[
    datetime | constr(pattern=REGEX_ISODATE), AfterValidator(datetime_validate)
]


class CustomModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
