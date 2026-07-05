from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import auth_service

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=201,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return auth_service.register(
        db=db,
        full_name=request.full_name,
        email=request.email,
        password=request.password,
        phone=request.phone,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return auth_service.login(
        db=db,
        email=request.email,
        password=request.password,
    )
