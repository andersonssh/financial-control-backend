from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from jose.exceptions import JWTError
import time

from app.routers import registers
from app.routers.auth import route as auth_route
from app.core import auth
import logging
import socket
from logging.handlers import SysLogHandler
import os
syslog = SysLogHandler(address=(os.getenv("PAPERTRAIL_HOST"), int(os.getenv("PAPERTRAIL_PORT"))))
format = '%(asctime)s finantrol: %(message)s'
formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
syslog.setFormatter(formatter)

logger = logging.getLogger("finantrol")
logger.addHandler(syslog)
logger.setLevel(logging.INFO)

app = FastAPI()

@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user_data = auth.decode_token(token)
            logger.info(f"{request.method} {request.url.path} - user: {user_data.get('email')} - status: {response.status_code} - time: {process_time:.2f}s")
        else:
            logger.info(f"{request.method} {request.url.path} status: {response.status_code} - time: {process_time:.2f}s")
    except Exception:
        logger.info(f"{request.method} {request.url.path} status: {response.status_code} - time: {process_time:.2f}s")
    
    return response

origins = [
    "https://finantrol.codedevolution.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(registers.router)
app.include_router(auth_route.router)


@app.get("/")
def main_route():
    return {}
