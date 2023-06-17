from typing import Any

from pydantic import BaseSettings, PostgresDsn, root_validator

from app.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn

    SITE_DOMAIN: str = "*"

    ENVIRONMENT: Environment = Environment.LOCAL

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"


settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs