from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(levelname)-8s - %(message)s"
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_FORMAT


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class SuperUser(BaseModel):
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    registered_at: datetime = datetime.now(timezone.utc)


class SMTP(BaseModel):
    user: str
    password: str
    host: str
    port: int


class Redis(BaseModel):
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True,
        env_file=(".env.template.", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    db: DataBaseConfig
    access_token: AccessToken
    superuser: SuperUser
    smtp: SMTP
    redis: Redis


settings = Settings()  # type: ignore
