from datetime import datetime

from bson.objectid import ObjectId

from app.models.base import CustomDatetime, CustomModel, PyObjectId


class TestCustomModel:
    def test_custom_model_parsing_to_str(self):
        class CustomModelTest(CustomModel):
            datetime_field: CustomDatetime
            pyobjectid_field: PyObjectId

        custom_model = CustomModelTest(
            datetime_field=datetime.fromisoformat("2001-01-01 01:01:01"),
            pyobjectid_field=ObjectId("65309236cc11b109bbe4b0d5"),
        )
        assert custom_model.model_dump() == {
            "datetime_field": "2001-01-01 01:01:01",
            "pyobjectid_field": "65309236cc11b109bbe4b0d5",
        }

    def test_custom_model_parsing_to_original_type(self):
        class CustomModelTest(CustomModel):
            datetime_field: CustomDatetime
            pyobjectid_field: PyObjectId

        custom_model = CustomModelTest(
            datetime_field="2001-01-01 01:01:01",
            pyobjectid_field="65309236cc11b109bbe4b0d5",
        )
        assert custom_model.model_dump() == {
            "datetime_field": datetime.fromisoformat("2001-01-01 01:01:01"),
            "pyobjectid_field": ObjectId("65309236cc11b109bbe4b0d5"),
        }
