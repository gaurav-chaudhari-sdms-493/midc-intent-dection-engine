from sqlalchemy.orm import Session
import uuid

from app.models.user import User


class UserRepository:

    def create_user(
        self,
        db: Session,
        user: User,
    ) -> User:
        """
        Adds a new User instance to the database and commits.
        """
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        """
        Retrieves a User by their email address.
        """
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_id(
        self,
        db: Session,
        user_id: uuid.UUID,
    ) -> User | None:
        """
        Retrieves a User by their ID.
        """
        return db.get(User, user_id)

    def email_exists(
        self,
        db: Session,
        email: str,
    ) -> bool:
        """
        Checks if a user with the given email already exists.
        """
        return self.get_by_email(db, email) is not None

# The user repository is now a class, not a singleton instance.
# We will instantiate it where needed, or use a dependency injection system.
# For now, the AuthService will create its own instance.
