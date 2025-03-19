from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from jose.exceptions import JWTError
import logging

from app.routers import registers
from app.routers.auth import route as auth_route
from app.core import auth

# Configurando o sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://finantrol.com",
    "https://finantrol-mu.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def log_user_email(request: Request, call_next):
    response = await call_next(request)
    
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        try:
            payload = auth.decode_token(token)
            email = payload.get("email")
            if email:
                logger.info(f"Request to {request.url.path} by user: {email}")
        except JWTError:
            logger.warning(f"Invalid token provided for request to {request.url.path}")
    else:
        logger.info(f"Unauthenticated request to {request.url.path}")
    
    return response

app.include_router(registers.router)
app.include_router(auth_route.router)


@app.get("/")
def main_route():
    return {}
