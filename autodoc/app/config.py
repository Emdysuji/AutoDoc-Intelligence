"""Application configuration management."""
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = "AutoDoc Intelligence"
    app_env: str = "development"
    debug: bool = False
    api_prefix: str = ""

    database_url: str = Field(default="postgresql+psycopg2://autodoc:autodoc@db:5432/autodoc")
    local_storage_path: Path = Field(default=Path("storage"))
    max_file_size_mb: int = 10
    cors_origins: str = "*"

    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    ocr_engine: str = "tesseract"
    tesseract_cmd: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
