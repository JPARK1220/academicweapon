from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    OPENROUTER_API_KEY: str

    SUPABASE_URL: str
    SUPABASE_KEY: str

    MONGODB_URI: str

    SITE_DOMAIN: str = "localhost.com"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # SENTRY_DSN: str | None = None

    # Development Cors Settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    # CORS_ORIGINS_REGEX: str | None = None

    APP_VERSION: str = "1.0"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Config()
