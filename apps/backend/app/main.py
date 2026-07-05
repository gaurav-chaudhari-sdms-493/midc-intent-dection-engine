from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.core.exceptions import UserAlreadyExists, InvalidCredentials
from app.core.exception_handlers import (
    user_already_exists_handler,
    invalid_credentials_handler,
)

app = FastAPI(
    title="MIDC Intent Detection Engine",
)

app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
app.add_exception_handler(InvalidCredentials, invalid_credentials_handler)

app.include_router(auth_router)
