import logging
import json

from typing import TYPE_CHECKING

from config import settings
from common import (
    create_user_in_fastapi,
    UsersUpdatesRabbit,
)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


log = logging.getLogger(__name__)


def process_new_message(
    ch: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.debug("ch: %s", ch)
    log.debug("method: %s", method)
    log.debug("properties: %s", properties)
    log.debug("body: %s", body)

    user_data = json.loads(body)

    log.warning("[ ] Start checking new user %r", body)

    create_user_in_fastapi(user_data=user_data)

    log.info("Finished processing message %r, sending ack!", body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    log.warning(
        "[X] Finished checking user. message %r OK!",
        body,
    )


def consume():
    with UsersUpdatesRabbit() as rabbit:
        rabbit.consume_messages(
            message_callback=process_new_message,
            queue_name=settings.rabbitmq.queue_name,
        )


if __name__ == "__main__":
    try:
        consume()
    except KeyboardInterrupt:
        log.warning("Goodbye!")
