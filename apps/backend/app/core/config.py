from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[4]
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str
    ENVIRONMENT: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            "postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()