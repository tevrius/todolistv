from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения: читаются из переменных окружения и файла .env."""

    # Строка подключения к PostgreSQL, например:
    # postgresql+asyncpg://todo:todo@localhost:5432/todo
    database_url: str = "postgresql+asyncpg://todo:todo@localhost:5432/todo"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
