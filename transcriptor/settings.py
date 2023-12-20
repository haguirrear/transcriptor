from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    SUPABASE_URL: str
    SUPABASE_API_KEY: str
    OPEN_AI_API_KEY: str
    SECRET_KEY: str = "insecure-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
