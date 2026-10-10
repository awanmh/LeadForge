from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    database_url: str = Field(
        default="postgresql+psycopg://leadforge_app_user:app_secure_pass_dev_only@localhost:5432/leadforge_app",
        alias="DATABASE_URL"
    )
    max_request_bytes: int = Field(default=1048576, alias="MAX_REQUEST_BYTES")
    rate_limit_per_minute: int = Field(default=10, alias="RATE_LIMIT_PER_MINUTE")
    trusted_proxies: str = Field(default="127.0.0.1", alias="TRUSTED_PROXIES")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
