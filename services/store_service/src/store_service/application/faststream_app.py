import aio_pika
from faststream import FastStream
from faststream.specification import AsyncAPI

from common.messaging import (
    create_product_exch_init,
    create_product_queue_init,
    delete_product_exch_init,
    delete_product_queue_init,
    rabbit_broker,
    update_product_exch_init,
    update_product_queue_init,
)
from store_service.consumers import inventory_routes  # noqa: F401

app = FastStream(rabbit_broker, specification=AsyncAPI())


@app.on_startup
async def initialize_app() -> None:
    from common.persistence import PostgresSessionFactory

    PostgresSessionFactory.initialize()

    create_product_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=create_product_queue_init)
    await create_product_queue.bind(exchange=create_product_exch_init)

    update_product_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=update_product_queue_init)
    await update_product_queue.bind(exchange=update_product_exch_init)

    delete_product_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=delete_product_queue_init)
    await delete_product_queue.bind(exchange=delete_product_exch_init)
