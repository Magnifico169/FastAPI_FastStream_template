import logging
import sys

from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter

from app.settings import get_rabbitmq_settings

rabbitmq_settings = get_rabbitmq_settings()
rabbitmq_uri = rabbitmq_settings.get_rabbitmq_uri()

messages_exchange = RabbitExchange("messages_exchange", type=ExchangeType.DIRECT, durable=True)
messages_queue = RabbitQueue("messages_queue", durable=True)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

rabbit_router = RabbitRouter(url=rabbitmq_uri, logger=root_logger)
rabbit_broker = rabbit_router.broker
