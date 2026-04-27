from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseSettings):
    """Optional shared app-level settings (e.g. log level)."""

    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")

    LOG_LEVEL: str = Field(default="INFO", description="Root log level")


@lru_cache
def get_logging_settings() -> LoggingSettings:
    """Get logging settings."""
    return LoggingSettings()  # type: ignore[call-arg]
