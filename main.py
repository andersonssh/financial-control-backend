from fastapi import FastAPI

from app.routers.registers import registers_router

app = FastAPI()

app.include_router(registers_router)
