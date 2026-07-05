from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    ENVIRONMENT: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Default for local development, overridden in Docker.
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings():
    # The .env file is in the parent directory of the 'app' directory.
    # __file__ -> /path/to/project/apps/backend/app/core/config.py
    # .parent -> /path/to/project/apps/backend/app/core
    # .parent -> /path/to/project/apps/backend/app
    # .parent -> /path/to/project/apps/backend
    env_path = Path(__file__).parent.parent.parent / ".env"
    return Settings(_env_file=env_path)


settings = get_settings()
