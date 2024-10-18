from pika import ConnectionParameters, PlainCredentials
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from config import settings

from .exc import RabbitException


class RabbitBase:
    connection_parameters = ConnectionParameters(
        host=settings.rabbitmq.host,
        port=settings.rabbitmq.port,
        credentials=PlainCredentials(
            username=settings.rabbitmq.username,
            password=settings.rabbitmq.password,
        ),
    )

    def __init__(
        self,
        connection_parameters: ConnectionParameters = connection_parameters,
    ) -> None:
        self.connection_parameters = connection_parameters
        self._connection: BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    def get_connection(self) -> BlockingConnection:
        return BlockingConnection(self.connection_parameters)

    @property
    def channel(self) -> BlockingChannel:
        if self._channel is None:
            raise RabbitException("Please use context manager for Rabbit helper.")
        return self._channel

    def __enter__(self):
        self._connection = self.get_connection()
        self._channel = self._connection.channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._channel.is_open:
            self._channel.close()

        if self._connection.is_open:
            self._connection.close()
