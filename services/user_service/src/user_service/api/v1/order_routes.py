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


@order_router.post(
    "/order_status",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["order"],
)
async def get_order_status(message: OrderStatusRequestSchema) -> MessageStatusResponse:
    """
    Start async lookup of a single order (published to the worker queue).

    POST is used because a JSON body is required; GET cannot carry a body in browsers.

    :param message: Request with order id / user id as required by the worker
    :return: 202 with PROCESSING; result is completed asynchronously
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


@order_router.post(
    "/orders_status",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["order"],
)
async def get_orders_status(message: OrderStatusRequestSchema) -> MessageStatusResponse:
    """
    Start async lookup of orders for a user (published to the worker queue).

    POST is used because a JSON body is required; GET cannot carry a body in browsers.

    :param message: Request with user_id for the list query
    :return: 202 with PROCESSING; result is completed asynchronously
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
    Enqueue new order creation: publish to the user-service worker for stock check and persist.

    :param message: Order and product lines to create
    :return: 202 with PROCESSING; outcome is processed by the consumer
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
    Enqueue order cancellation: publish delete request to the worker queue.

    :param message: Order reference to cancel
    :return: 202 with PROCESSING; deletion runs asynchronously
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
    Enqueue order update: publish changed fields to the worker queue.

    :param message: Order payload with id and fields to update
    :return: 202 with PROCESSING; update runs asynchronously
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
