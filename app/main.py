from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.registers import registers_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"])
app.include_router(registers_router)
