import logging
import sys

from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit import RabbitQueue, RabbitExchange, ExchangeType

from models.settings.rabbitmq_settings import get_rabbitmq_settings

rabbitmq_settings = get_rabbitmq_settings()
rabbitmq_uri = rabbitmq_settings.get_rabbitmq_uri()


create_user_exch_init = RabbitExchange("create_user_exchange", type=ExchangeType.DIRECT, durable=True)
create_user_queue_init = RabbitQueue("create_user_queue", durable=True)

create_order_exch_init = RabbitExchange("create_order_exchange", type=ExchangeType.DIRECT, durable=True)
create_order_queue_init = RabbitQueue("create_order_queue", durable=True)

update_order_exch_init = RabbitExchange("update_order_exchange", type=ExchangeType.DIRECT, durable=True)
update_order_queue_init = RabbitQueue("update_order_queue", durable=True)

cancel_order_exch_init = RabbitExchange("cancel_order_exchange", type=ExchangeType.DIRECT, durable=True)
cancel_order_queue_init = RabbitQueue("cancel_order_queue", durable=True)

get_order_into_exch_init = RabbitExchange("get_order_into_exchange", type=ExchangeType.DIRECT, durable=True)
get_order_queue_init = RabbitQueue("get_order_queue", durable=True)

get_orders_into_exch_init = RabbitExchange("get_orders_into_exchange", durable=True)
get_orders_queue_init = RabbitQueue("get_orders_queue", durable=True)


create_product_exch_init = RabbitExchange("create_product_exchange", type=ExchangeType.DIRECT, durable=True)
create_product_queue_init = RabbitQueue("create_product_queue", durable=True)

update_product_exch_init = RabbitExchange("update_product_exchange", type=ExchangeType.DIRECT, durable=True)
update_product_queue_init = RabbitQueue("update_product_queue", durable=True)

delete_product_exch_init = RabbitExchange("delete_product_exchange", type=ExchangeType.DIRECT, durable=True)
delete_product_queue_init = RabbitQueue("delete_product_queue", durable=True)

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
