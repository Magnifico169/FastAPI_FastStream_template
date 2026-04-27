from fastapi import APIRouter

from common.constants import MessageStatus
from common.messaging import (
    create_product_exch_init,
    create_product_queue_init,
    delete_product_exch_init,
    delete_product_queue_init,
    rabbit_broker,
    update_product_exch_init,
    update_product_queue_init,
)
from common.schemas import MessageStatusResponse, Product

inventory_router = APIRouter()


@inventory_router.post("/product", tags=["inventory"])
async def create_product(
    message: Product,
) -> MessageStatusResponse:
    """
    Enqueue product creation: publish to the inventory worker queue.

    :param message: Product payload
    :return: OK status after the message is accepted for delivery
    """

    await rabbit_broker.publish(
        message=message,
        queue=create_product_queue_init,
        exchange=create_product_exch_init,
    )
    return MessageStatusResponse(message=MessageStatus.OK)


@inventory_router.delete(
    "/product",
    tags=["inventory"],
    response_model=MessageStatusResponse,
)
async def delete_product(
    message: Product,
) -> MessageStatusResponse:
    """
    Enqueue product deletion: publish to the inventory worker queue.

    :param message: Product to remove (e.g. by id)
    :return: OK status after the message is accepted for delivery
    """

    await rabbit_broker.publish(
        message=message,
        queue=delete_product_queue_init,
        exchange=delete_product_exch_init,
    )
    return MessageStatusResponse(message=MessageStatus.OK)


@inventory_router.put("/product", tags=["inventory"])
async def update_product(
    message: Product,
) -> MessageStatusResponse:
    """
    Enqueue product update: publish to the inventory worker queue.

    :param message: Product fields to apply
    :return: OK status after the message is accepted for delivery
    """

    await rabbit_broker.publish(
        message=message,
        queue=update_product_queue_init,
        exchange=update_product_exch_init,
    )
    return MessageStatusResponse(message=MessageStatus.OK)
