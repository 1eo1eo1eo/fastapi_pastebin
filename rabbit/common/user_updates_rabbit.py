import logging
from typing import (
    Callable,
    TYPE_CHECKING,
)
from pika.exchange_type import ExchangeType

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import (
        Basic,
        BasicProperties,
    )


from .base import RabbitBase
from config import settings


log = logging.getLogger(__name__)


class UsersUpdatesRabbitMixin:
    channel: "BlockingChannel"

    def declare_users_updates_exchange(self):
        self.channel.exchange_declare(
            exchange=settings.rabbitmq.exchange_name, exchange_type=ExchangeType.fanout
        )

    def declare_queue_for_users_updates(
        self,
        queue_name: str = "",
        exclusive: bool = True,
    ):
        self.declare_users_updates_exchange()
        queue = self.channel.queue_declare(
            queue=queue_name,
            exclusive=exclusive,
        )
        q_name = queue.method.queue
        self.channel.queue_bind(
            exchange=settings.rabbitmq.exchange_name,
            queue=q_name,
        )
        return q_name

    def consume_messages(
        self,
        message_callback: Callable[
            [
                "BlockingChannel",
                "Basic.Deliver",
                "BasicProperties",
                bytes,
            ],
            None,
        ],
        queue_name: str = "",
        prefetch_count=1,
    ):
        self.channel.basic_qos(prefetch_count=prefetch_count)
        q_name = self.declare_queue_for_users_updates(
            queue_name=queue_name,
            exclusive=not queue_name,
        )
        self.channel.basic_consume(
            queue=q_name,
            on_message_callback=message_callback,
        )
        log.warning("Waiting for messages...")
        self.channel.start_consuming()


class UsersUpdatesRabbit(UsersUpdatesRabbitMixin, RabbitBase):
    pass
