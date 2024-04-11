from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    SUPABASE_URL: str
    SUPABASE_API_KEY: str
    OPEN_AI_API_KEY: str
    SECRET_KEY: str = "insecure-key"

    SITE_HOST: str = "http://localhost:8000"

    MERCADO_PAGO_ACCESS_TOKEN: str | None = None
    MERCADO_PAGO_PUBLIC_KEY: str | None = None
    INVOICE_NAME: str = "THE REVOL"

    SUPABASE_JWT_KEY: str = "insecure-key2"

    DATABASE_DRIVER: Literal["asyncpg", "psycopg"] = "asyncpg"
    DATABASE_USER: str
    DATABASE_PSW: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    REDIS_URL: str | None = None

    SESSION_DURATION_DAYS: int = 10
    MAX_REQUEST_PER_MINUTE: int = 5

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+{self.DATABASE_DRIVER}://{self.DATABASE_USER}:{self.DATABASE_PSW}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()  # type: ignore
