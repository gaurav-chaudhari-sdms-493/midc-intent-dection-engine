from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import decode_token
from app.repositories import user_repository
from app.models.enums import UserStatus, UserRole

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    try:
        payload = decode_token(token)

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user = user_repository.get_by_id(
        db,
        payload["sub"],
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


def get_current_active_user(

    current_user=Depends(get_current_user),

):

    if current_user.status != UserStatus.ACTIVE:

        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    return current_user


class RoleChecker:

    def __init__(self, allowed_roles):

        self.allowed_roles = allowed_roles

    def __call__(self, user=Depends(get_current_active_user)):

        if user.role not in self.allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        return user


InvestorOnly = RoleChecker(
    [UserRole.INVESTOR]
)

OfficerOnly = RoleChecker(
    [UserRole.OFFICER]
)

AdminOnly = RoleChecker(
    [UserRole.ADMIN]
)
