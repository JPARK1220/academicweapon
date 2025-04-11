from pydantic import field_validator
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    OPENROUTER_API_KEY: str

    SUPABASE_URL: str
    SUPABASE_KEY: str

    MONGODB_URI: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    SITE_DOMAIN: str = "localhost.com"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # SENTRY_DSN: str | None = None

    # Development Cors Settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    # CORS_ORIGINS_REGEX: str | None = None

    APP_VERSION: str = "1.0"

    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_BUCKET: str

    class Config:
        env_file = ".env"
        case_sensitive = True



settings = Config()
