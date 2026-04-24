import aio_pika

from faststream import FastStream
from faststream.specification import AsyncAPI

from models.rabbit.rabbit import (
    rabbit_broker,
    create_order_exch_init,
    create_order_queue_init,
    create_user_exch_init,
    create_user_queue_init,
    delete_order_exch_init,
    delete_order_queue_init,
    delete_user_exch_init,
    delete_user_queue_init,
    get_orders_into_exch_init,
    get_orders_queue_init,
    update_order_exch_init,
    update_order_queue_init,
)


app = FastStream(rabbit_broker, specification=AsyncAPI())


@app.on_startup
async def initialize_app() -> None:
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

    delete_order_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=delete_order_exch_init,
    )
    delete_order_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=delete_order_queue_init)
    await delete_order_queue.bind(exchange=delete_order_exchange)

    get_orders_into_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=get_orders_into_exch_init,
    )
    get_orders_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=get_orders_queue_init)
    await get_orders_queue.bind(exchange=get_orders_into_exchange)

    delete_user_exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
        exchange=delete_user_exch_init,
    )
    delete_user_queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(queue=delete_user_queue_init)
    await delete_user_queue.bind(exchange=delete_user_exchange)
