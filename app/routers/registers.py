from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException

from app.core import database
from app.models.registers import (GetRegistersModel, PatchRegisterModel,
                                  RegisterBaseModel, RegisterModel)

router = APIRouter(tags=["users"])


@router.post(
    "/registers",
    status_code=201,
    response_model_by_alias=True,
    response_model_exclude_none=True,
)
def post_registers(register: RegisterBaseModel) -> RegisterModel:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    new_register = RegisterModel(
        **register.model_dump(by_alias=True), user_id=user_id
    ).model_dump(by_alias=True)
    inserted_document = database.insert_one("registers", new_register)
    return RegisterModel(**inserted_document)


@router.get(
    "/registers", response_model_by_alias=True, response_model_exclude_none=True
)
def get_registers() -> GetRegistersModel:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    registers = database.find("registers", {"user_id": user_id})
    return GetRegistersModel(data=registers)


@router.put("/registers/{register_id}", status_code=204)
def put_register(register_id: str, register: RegisterBaseModel) -> None:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    # todo: implementar logica para impedir mudança de tipo do registro
    update_result = database.update_one(
        "registers",
        {"_id": ObjectId(register_id), "user_id": user_id},
        register.model_dump(by_alias=True, exclude_unset=True),
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Register not found")
    return None


@router.patch("/registers/{register_id}", status_code=204)
def patch_register(register_id: str, register: PatchRegisterModel) -> None:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    update_result = database.update_one(
        "registers",
        {"_id": ObjectId(register_id), "user_id": user_id},
        register.model_dump(by_alias=True, exclude_unset=True),
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Register not found")
    return None


@router.delete("/registers/{register_id}", status_code=204)
def delete_register(register_id: str) -> None:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")

    if not database.delete_one(
        "registers", {"user_id": user_id, "_id": ObjectId(register_id)}
    ):
        raise HTTPException(status_code=404, detail="Register not found")
    return None
