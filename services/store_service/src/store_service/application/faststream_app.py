from faststream import FastStream

from common.messaging import (
    create_product_exch_init,
    create_product_queue_init,
    delete_product_exch_init,
    delete_product_queue_init,
    rabbit_broker,
    root_logger,
    update_product_exch_init,
    update_product_queue_init,
)
from store_service.consumers import inventory_routes  # noqa: F401
from common.persistence import PostgresSessionFactory

app = FastStream(rabbit_broker)


@app.on_startup
async def initialize_db() -> None:
    """Initialize database connection."""
    await PostgresSessionFactory.initialize()
    root_logger.info("initialize db connection")


@app.after_startup
async def initialize_app() -> None:
    """
    Declare product inventory exchanges/queues and bind them on broker startup.

    :return: None
    """

    create_product_exchange = await rabbit_broker.declare_exchange(exchange=create_product_exch_init)
    create_product_queue = await rabbit_broker.declare_queue(queue=create_product_queue_init)
    await create_product_queue.bind(exchange=create_product_exchange)

    update_product_exchange = await rabbit_broker.declare_exchange(exchange=update_product_exch_init)
    update_product_queue = await rabbit_broker.declare_queue(queue=update_product_queue_init)
    await update_product_queue.bind(exchange=update_product_exchange)

    delete_product_exchange = await rabbit_broker.declare_exchange(exchange=delete_product_exch_init)
    delete_product_queue = await rabbit_broker.declare_queue(queue=delete_product_queue_init)
    await delete_product_queue.bind(exchange=delete_product_exchange)
