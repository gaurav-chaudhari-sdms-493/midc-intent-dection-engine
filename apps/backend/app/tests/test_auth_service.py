import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import UserAlreadyExists, InvalidCredentials, InactiveUser
from app.models.user import User, UserStatus
# Updated import to reflect the new auth package structure
from app.auth.service import AuthService

# Reusable user data
USER_DATA = {
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "Password@123",
    "phone": "1234567890",
}


@pytest.fixture
def auth_service() -> AuthService:
    """Fixture to provide a new instance of the AuthService for each test."""
    return AuthService()


def test_register_success(db_session: Session, auth_service: AuthService):
    """
    Test successful user registration.
    """
    auth_response = auth_service.register(db=db_session, **USER_DATA)

    assert auth_response.email == USER_DATA["email"]
    assert auth_response.role == "INVESTOR"
    assert auth_response.tokens.access_token
    assert auth_response.tokens.refresh_token

    user_in_db = db_session.query(User).filter(User.email == USER_DATA["email"]).first()
    assert user_in_db is not None
    assert user_in_db.full_name == USER_DATA["full_name"]
    assert user_in_db.is_active is True


def test_register_duplicate_email(db_session: Session, auth_service: AuthService):
    """
    Test registration fails if the email already exists.
    """
    auth_service.register(db=db_session, **USER_DATA)

    with pytest.raises(UserAlreadyExists):
        auth_service.register(db=db_session, **USER_DATA)


def test_login_success(db_session: Session, auth_service: AuthService):
    """
    Test successful user login for an active user.
    """
    auth_service.register(db=db_session, **USER_DATA)

    auth_response = auth_service.login(
        db=db_session, email=USER_DATA["email"], password=USER_DATA["password"]
    )

    assert auth_response.email == USER_DATA["email"]
    assert auth_response.tokens.access_token


def test_login_invalid_email(db_session: Session, auth_service: AuthService):
    """
    Test login fails with a non-existent email.
    """
    with pytest.raises(InvalidCredentials):
        auth_service.login(
            db=db_session, email="wrong@email.com", password="anypassword"
        )


def test_login_wrong_password(db_session: Session, auth_service: AuthService):
    """
    Test login fails with the correct email but wrong password.
    """
    auth_service.register(db=db_session, **USER_DATA)

    with pytest.raises(InvalidCredentials):
        auth_service.login(
            db=db_session, email=USER_DATA["email"], password="WrongPassword"
        )


def test_login_inactive_user_fails(db_session: Session, auth_service: AuthService):
    """
    Test login fails if a user is explicitly made inactive.
    """
    auth_service.register(db=db_session, **USER_DATA)

    # Manually set the user to inactive
    # Corrected to use the new 'repository' attribute name
    user = auth_service.repository.get_by_email(db_session, USER_DATA["email"])
    user.status = UserStatus.INACTIVE
    db_session.commit()

    with pytest.raises(InactiveUser):
        auth_service.login(
            db=db_session, email=USER_DATA["email"], password=USER_DATA["password"]
        )
