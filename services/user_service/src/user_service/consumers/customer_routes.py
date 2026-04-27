import logging

from common.domain import Order, User
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
    update_order_exch_init,
    update_order_queue_init,
)
from user_service.services import AccountServiceDep, UserServiceDep

logger = logging.getLogger(__name__)


@rabbit_broker.subscriber(
    queue=create_user_queue_init,
    exchange=create_user_exch_init,
)
async def create_user(message: User, account_service: AccountServiceDep) -> None:
    await account_service.create_user(message)
    logger.info("User %s successfully created", message)


@rabbit_broker.subscriber(
    queue=create_order_queue_init,
    exchange=create_order_exch_init,
)
async def create_order(message: Order, user_service: UserServiceDep) -> None:
    await user_service.create_order(message)
    logger.info("Order %s successfully created", message)


@rabbit_broker.subscriber(
    queue=update_order_queue_init,
    exchange=update_order_exch_init,
)
async def update_order(
    message: Order,
    user_service: UserServiceDep,
) -> None:
    order = await user_service.edit_order(message)
    logger.info("Order %s successfully updated", order)


@rabbit_broker.subscriber(
    queue=cancel_order_queue_init,
    exchange=cancel_order_exch_init,
)
async def cancel_order(message: Order, user_service: UserServiceDep) -> None:
    await user_service.cancel_order(message)
    logger.info("Order %s successfully deleted", message)


@rabbit_broker.subscriber(
    queue=get_orders_queue_init,
    exchange=get_orders_into_exch_init,
)
async def get_orders(
    message: Order,
    user_service: UserServiceDep,
) -> None:
    await user_service.get_orders_list(message)
    logger.info("Order for user %s successfully retrieved", message.user_id)


@rabbit_broker.subscriber(
    queue=get_order_queue_init,
    exchange=get_order_into_exch_init,
)
async def get_order(
    message: Order,
    user_service: UserServiceDep,
) -> None:
    await user_service.get_order(message)
    logger.info("Order for user %s successfully retrieved", message.user_id)
