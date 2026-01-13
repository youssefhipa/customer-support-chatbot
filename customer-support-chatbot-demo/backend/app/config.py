from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application configuration loaded from environment variables."""

    APP_NAME: str = "DemoShop Support Bot"
    BACKEND_PORT: int = 8000
    PROXY_BASE_URL: str = "http://localhost:3003"
    PROXY_CHAT_PATH: str = "/v1/chat/completions"
    PROXY_API_KEY: str | None = None
    MODEL_NAME: str = "gpt-4o-mini"
    REQUEST_TIMEOUT_SECONDS: int = 30

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> AppSettings:
    """Return a cached settings instance."""

    return AppSettings()
