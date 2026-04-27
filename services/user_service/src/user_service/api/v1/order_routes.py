from fastapi import APIRouter, status

from common.constants import MessageStatus
from common.messaging import (
    cancel_order_exch_init,
    cancel_order_queue_init,
    create_order_exch_init,
    create_order_queue_init,
    get_order_into_exch_init,
    get_order_queue_init,
    get_orders_into_exch_init,
    get_orders_queue_init,
    rabbit_broker,
    update_order_exch_init,
    update_order_queue_init,
)
from common.schemas import MessageStatusResponse, OrderStatusRequestSchema

order_router = APIRouter()


@order_router.get(
    "/order_status",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["order"],
)
async def get_order_status(message: OrderStatusRequestSchema) -> MessageStatusResponse:
    """
    Get order status.

    :param message:
    :return:
    """

    await rabbit_broker.publish(
        message=message,
        queue=get_order_queue_init,
        exchange=get_order_into_exch_init,
    )
    return MessageStatusResponse(
        message=MessageStatus.PROCESSING,
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.get(
    "/orders_status",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["order"],
)
async def get_orders_status(message: OrderStatusRequestSchema) -> MessageStatusResponse:
    """
    Get orders status.

    :param message:
    :return:
    """

    await rabbit_broker.publish(
        message=message,
        queue=get_orders_queue_init,
        exchange=get_orders_into_exch_init,
    )
    return MessageStatusResponse(
        message=MessageStatus.PROCESSING,
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.post(
    "/order",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["order"],
)
async def create_order(message: OrderStatusRequestSchema) -> MessageStatusResponse:
    """
    Create new order.

    :param message:
    :return:
    """

    await rabbit_broker.publish(
        message=message,
        queue=create_order_queue_init,
        exchange=create_order_exch_init,
    )
    return MessageStatusResponse(
        message=MessageStatus.PROCESSING,
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.delete(
    "/order",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["order"],
)
async def cancel_order(message: OrderStatusRequestSchema) -> MessageStatusResponse:
    """
    Cancel order.

    :param message:
    :return:
    """

    await rabbit_broker.publish(
        message=message,
        queue=cancel_order_queue_init,
        exchange=cancel_order_exch_init,
    )
    return MessageStatusResponse(
        message=MessageStatus.PROCESSING,
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.put(
    "/order",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["order"],
)
async def update_order(message: OrderStatusRequestSchema) -> MessageStatusResponse:
    """
    Update order.

    :param message:
    :return:
    """

    await rabbit_broker.publish(
        message=message,
        queue=update_order_queue_init,
        exchange=update_order_exch_init,
    )
    return MessageStatusResponse(
        message=MessageStatus.PROCESSING,
        status=status.HTTP_202_ACCEPTED,
    )
