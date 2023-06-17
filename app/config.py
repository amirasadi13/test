from pydantic import BaseSettings, PostgresDsn

from app.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn

    SITE_DOMAIN: str = "*"

    ENVIRONMENT: Environment = Environment.LOCAL
    APP_VERSION: str = "1"


settings = Config()
