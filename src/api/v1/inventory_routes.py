from fastapi import APIRouter

from infrastructure.rabbit.rabbit import (
    create_product_exch_init,
    create_product_queue_init,
    delete_product_exch_init,
    delete_product_queue_init,
    rabbit_broker,
    update_product_exch_init,
    update_product_queue_init,
)
from core.models.schemas import Product, MessageStatusResponse
from core.constants import MessageStatus

inventory_router = APIRouter()


@inventory_router.post("/product", tags=["inventory"], response_model=MessageStatusResponse)
async def create_product(
    message: Product,
) -> MessageStatusResponse:
    """
    Create a new product.

    :param message:
    :return:
    """
    await rabbit_broker.publish(
        message=message,
        queue=create_product_queue_init,
        exchange=create_product_exch_init,
    )
    return MessageStatusResponse(message=MessageStatus.OK)


@inventory_router.delete(
    "/product/{product_id}",
    tags=["inventory"],
    response_model=MessageStatusResponse,
)
async def delete_product(
    message: Product,
) -> MessageStatusResponse:
    """
    Delete an existing product.

    :param message:
    :return:
    """

    await rabbit_broker.publish(
        message=message,
        queue=delete_product_queue_init,
        exchange=delete_product_exch_init,
    )
    return MessageStatusResponse(message=MessageStatus.OK)


@inventory_router.put("/product", tags=["inventory"], response_model=MessageStatusResponse)
async def update_product(
    message: Product,
) -> MessageStatusResponse:
    """
    Update an existing product.

    :param message:
    :return:
    """
    await rabbit_broker.publish(
        message=message,
        queue=update_product_queue_init,
        exchange=update_product_exch_init,
    )
    return MessageStatusResponse(message=MessageStatus.OK)
