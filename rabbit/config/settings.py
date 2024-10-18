import logging
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RabbitMQ(BaseModel):
    host: str
    port: int
    username: str
    password: str
    exchange: str
    exchange_name: str
    queue_name: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True,
        env_file=(".env.template.", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    rabbitmq: RabbitMQ

    @staticmethod
    def configure_logging(level: int = logging.INFO):
        logging.basicConfig(
            level=level,
            datefmt="%Y-%m-%d %H:%M:%S",
            format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(levelname)-8s - %(message)s",
        )


settings = Settings()  # type: ignore
