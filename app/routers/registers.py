from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app import database
from app.models.registers import (
    GetRegisters,
    PatchRegister,
    PostRegister,
    RegisterModel,
)

registers_router = APIRouter(prefix="/registers", tags=["users"])


@registers_router.post("/", status_code=201)
def post_registers(register: PostRegister) -> RegisterModel:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    new_register = register.model_dump(exclude_unset=True)
    new_register["user_id"] = user_id
    new_register["created_at"] = datetime.now()
    inserted_document = database.insert_one("registers", new_register)
    return RegisterModel(**inserted_document)


@registers_router.get("/")
def get_registers() -> GetRegisters:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")
    registers = database.find("registers", {"user_id": user_id})
    return GetRegisters(data=registers)


@registers_router.patch("/{register_id}", status_code=204)
def patch_register(register_id: str, register: PatchRegister) -> None:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")

    if not database.update_one(
        "registers",
        {"_id": ObjectId(register_id), "user_id": user_id},
        register.model_dump(exclude_unset=True),
    ):
        raise HTTPException(status_code=404, detail="Register not found")
    return None


@registers_router.delete("/{register_id}", status_code=204)
def delete_register(register_id: str) -> None:
    user_id = ObjectId("6526b0e5b30dbe90dcd63192")

    if not database.delete_one(
        "registers", {"user_id": user_id, "_id": ObjectId(register_id)}
    ):
        raise HTTPException(status_code=404, detail="Register not found")
    return None
