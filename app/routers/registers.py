from bson.objectid import ObjectId
from fastapi import APIRouter

from app import database
from app.models.registers import (
    GetRegisters,
    PatchRegister,
    PostRegister,
    RegisterModel,
)
from app.utils import get_now

registers_router = APIRouter(prefix="/registers", tags=["users"])


@registers_router.post("/", status_code=201)
def post_registers(register: PostRegister) -> RegisterModel:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    new_register = RegisterModel(
        **register.model_dump(exclude_unset=True),
        user_id=str(user_id),
        created_at=get_now()
    )
    inserted_document = database.insert_one(
        "registers", new_register.model_dump(exclude_unset=True)
    )
    return RegisterModel(**inserted_document)


@registers_router.get("/")
def get_registers() -> GetRegisters:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    registers = database.find("registers", {"user_id": user_id})
    return GetRegisters(data=registers)


@registers_router.patch("/{register_id}", status_code=204)
def patch_register(register_id: str, register: PatchRegister) -> None:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")

    database.update_one(
        "registers",
        {"_id": ObjectId(register_id), "user_id": user_id},
        register.model_dump(exclude_unset=True),
    )
    return None


@registers_router.delete("/{register_id}", status_code=204)
def delete_register(register_id: str) -> None:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")

    database.delete_one("registers", {"user_id": user_id, "_id": ObjectId(register_id)})
    return None
