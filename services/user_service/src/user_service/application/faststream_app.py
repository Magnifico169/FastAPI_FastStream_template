import aio_pika
from faststream import FastStream

from common.messaging import (
    cancel_order_exch_init,
    cancel_order_queue_init,
    create_order_exch_init,
    create_order_queue_init,
    create_user_exch_init,
    create_user_queue_init,
    get_order_into_exch_init,
    get_order_queue_init,
    get_orders_into_exch_init,
    get_orders_queue_init,
    rabbit_broker,
    root_logger,
    update_order_exch_init,
    update_order_queue_init,
)
from user_service.consumers import customer_routes  # noqa: F401
from common.persistence import PostgresSessionFactory


app = FastStream(rabbit_broker)


@app.on_startup
async def initialize_db() -> None:
    """Initialize database connection."""
    await PostgresSessionFactory.initialize()
    root_logger.info("initialize db connection")


@app.after_startup
async def start_application() -> None:
    """Initialize FastStream app."""

    create_user_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(exchange=create_user_exch_init)
    create_user_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=create_user_queue_init)
    await create_user_queue.bind(exchange=create_user_exchange)

    create_order_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=create_order_exch_init,
    )
    create_order_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=create_order_queue_init)
    await create_order_queue.bind(exchange=create_order_exchange)

    update_order_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=update_order_exch_init,
    )
    update_order_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=update_order_queue_init)
    await update_order_queue.bind(exchange=update_order_exchange)

    cancel_order_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=cancel_order_exch_init,
    )
    cancel_order_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=cancel_order_queue_init)
    await cancel_order_queue.bind(exchange=cancel_order_exchange)

    get_orders_into_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=get_orders_into_exch_init,
    )
    get_orders_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=get_orders_queue_init)
    await get_orders_queue.bind(exchange=get_orders_into_exchange)

    get_order_into_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=get_order_into_exch_init,
    )
    get_order_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=get_order_queue_init)
    await get_order_queue.bind(exchange=get_order_into_exchange)
