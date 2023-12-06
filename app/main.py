from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import registers
from app.routers.auth import route as auth_route

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(registers.router)
app.include_router(auth_route.router)
