import logging
from datetime import datetime, timezone
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


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
    db: DataBaseConfig
    access_token: AccessToken
    superuser: SuperUser
    smtp: SMTP
    redis: Redis

    @staticmethod
    def configure_logging(level: int = logging.INFO):
        logging.basicConfig(
            level=level,
            datefmt="%Y-%m-%d %H:%M:%S",
            format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(levelname)-8s - %(message)s",
        )


settings = Settings()  # type: ignore
