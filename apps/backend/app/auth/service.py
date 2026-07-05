import uuid
from sqlalchemy.orm import Session

# Exceptions can be shared, so they stay in core for now.
from app.core.exceptions import InvalidCredentials, UserAlreadyExists, InactiveUser
# Auth-specific utilities are moved into the auth package.
from app.auth.jwt import create_access_token, create_refresh_token
from app.auth.password import hash_password, verify_password
# Models are a shared resource.
from app.models.user import User, UserStatus
# The user repository is now the auth repository.
from app.auth.repository import AuthRepository
# Schemas are moved into the auth package.
from app.auth.schemas import AuthResponse, TokenResponse


class AuthService:
    def __init__(self):
        # The service now uses the dedicated AuthRepository.
        self.repository = AuthRepository()

    def _generate_tokens(self, user: User) -> TokenResponse:
        """
        Generate access and refresh tokens for a user.
        """
        access = create_access_token(str(user.id), user.role.value)
        refresh = create_refresh_token(str(user.id), user.role.value)
        return TokenResponse(access_token=access, refresh_token=refresh)

    def register(
        self,
        db: Session,
        *,
        full_name: str,
        email: str,
        password: str,
        phone: str | None = None,
    ) -> AuthResponse:
        """
        Register a new user, hash their password, and return with JWT tokens.
        """
        if self.repository.email_exists(db, email):
            raise UserAlreadyExists("An account with this email already exists.")

        user = User(
            id=uuid.uuid4(),
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            phone=phone,
            status=UserStatus.ACTIVE,
        )

        created_user = self.repository.create_user(db, user)
        tokens = self._generate_tokens(created_user)

        return AuthResponse(
            user_id=str(created_user.id),
            email=created_user.email,
            role=created_user.role.value,
            tokens=tokens,
        )

    def login(
        self,
        db: Session,
        *,
        email: str,
        password: str,
    ) -> AuthResponse:
        """
        Authenticate a user and return tokens.
        """
        user = self.repository.get_by_email(db, email)
        if not user:
            raise InvalidCredentials("Invalid email or password.")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentials("Invalid email or password.")

        if not user.is_active:
            raise InactiveUser("This user account is inactive.")

        tokens = self._generate_tokens(user)

        return AuthResponse(
            user_id=str(user.id),
            email=user.email,
            role=user.role.value,
            tokens=tokens,
        )
