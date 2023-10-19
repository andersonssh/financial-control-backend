from bson.objectid import ObjectId
from fastapi import APIRouter

from app import database
from app.models.registers import GetRegisters, PatchRegister

registers_router = APIRouter(prefix="/registers", tags=["users"])


@registers_router.get("/")
def get_registers():
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    registers = database.find("registers", {"user_id": user_id})
    return GetRegisters(data=registers).model_dump(exclude_unset=True)


@registers_router.patch("/{register_id}")
def patch_registers(register_id: str, register: PatchRegister):
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")

    database.update_one(
        "registers",
        {"_id": ObjectId(register_id), "user_id": user_id},
        register.model_dump(exclude_unset=True),
    )
    return {}, 204
