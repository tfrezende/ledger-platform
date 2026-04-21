from functools import lru_cache

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    database_url: PostgresDsn

    # Redis
    redis_url: RedisDsn

    # Cache
    balance_cache_ttl: int = 300  # seconds

    # Logging
    log_level: str = "INFO"

    # App
    app_env: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
