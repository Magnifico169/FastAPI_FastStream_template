from typing import Annotated, Final
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from infrastructure.rabbit import (
    create_order_exch_init,
    create_order_queue_init,
    delete_order_exch_init,
    delete_order_queue_init,
    get_order_into_exch_init,
    get_order_queue_init,
    get_orders_into_exch_init,
    get_orders_queue_init,
    rabbit_broker,
    update_order_exch_init,
    update_order_queue_init,
)
from models.schemas import OrderStatusRequestSchema, OrderStatusResponseSchema
from models.schemas.response import MessageStatusResponse

ALL_ORDERS_STATUS_ORDER_ID: Final[UUID] = UUID("00000000-0000-0000-0000-000000000000")

order_router = APIRouter()


@order_router.get(
    "/order_status",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MessageStatusResponse,
    tags=["order"],
)
async def get_order_status(
    order_id: Annotated[UUID, Query()],
    user_id: Annotated[UUID, Query()],
) -> MessageStatusResponse:
    if order_id == ALL_ORDERS_STATUS_ORDER_ID:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="invalid order_id for single order status",
        )
    payload = OrderStatusRequestSchema(order_id=order_id, user_id=user_id)
    await rabbit_broker.publish(
        payload,
        queue=get_order_queue_init,
        exchange=get_order_into_exch_init,
    )
    return MessageStatusResponse(
        message="processing",
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.get(
    "/orders_status",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MessageStatusResponse,
    tags=["order"],
)
async def get_orders_status(
    user_id: Annotated[UUID, Query()],
    order_id: Annotated[UUID, Query()] = ALL_ORDERS_STATUS_ORDER_ID,
) -> MessageStatusResponse:
    if order_id != ALL_ORDERS_STATUS_ORDER_ID:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="invalid order_id for orders list",
        )
    payload = OrderStatusRequestSchema(order_id=order_id, user_id=user_id)
    await rabbit_broker.publish(
        payload,
        queue=get_orders_queue_init,
        exchange=get_orders_into_exch_init,
    )
    return MessageStatusResponse(
        message="processing",
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.post(
    "/order",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MessageStatusResponse,
    tags=["order"],
)
async def create_order(body: OrderStatusResponseSchema) -> MessageStatusResponse:
    await rabbit_broker.publish(
        body,
        queue=create_order_queue_init,
        exchange=create_order_exch_init,
    )
    return MessageStatusResponse(
        message="processing",
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.delete(
    "/order",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MessageStatusResponse,
    tags=["order"],
)
async def delete_order(
    order_id: Annotated[UUID, Query()],
    user_id: Annotated[UUID, Query()],
) -> MessageStatusResponse:
    payload = OrderStatusRequestSchema(order_id=order_id, user_id=user_id)
    await rabbit_broker.publish(
        payload,
        queue=delete_order_queue_init,
        exchange=delete_order_exch_init,
    )
    return MessageStatusResponse(
        message="processing",
        status=status.HTTP_202_ACCEPTED,
    )


@order_router.put(
    "/order",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MessageStatusResponse,
    tags=["order"],
)
async def update_order(body: OrderStatusResponseSchema) -> MessageStatusResponse:
    await rabbit_broker.publish(
        body,
        queue=update_order_queue_init,
        exchange=update_order_exch_init,
    )
    return MessageStatusResponse(
        message="processing",
        status=status.HTTP_202_ACCEPTED,
    )
