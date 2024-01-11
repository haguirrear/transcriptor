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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
