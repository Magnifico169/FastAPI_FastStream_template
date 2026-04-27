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
    rabbit_router,
    update_order_exch_init,
    update_order_queue_init,
)
from user_service.services import AccountServiceDep, UserServiceDep

logger = logging.getLogger(__name__)


@rabbit_router.subscriber(
    queue=create_user_queue_init,
    exchange=create_user_exch_init,
)
async def create_user(message: User, account_service: AccountServiceDep) -> None:
    """
    Create new user (Rabbit consumer): persist the user from the queue message.

    :param message: User domain object from the broker
    :param account_service: Injected account service
    :return: None
    """

    await account_service.create_user(message)
    logger.info("User %s successfully created", message)


@rabbit_router.subscriber(
    queue=create_order_queue_init,
    exchange=create_order_exch_init,
)
async def create_order(message: Order, user_service: UserServiceDep) -> None:
    """
    Create new order: validate stock and persist the order for the user.

    :param message: Order domain object from the broker
    :param user_service: Injected user service
    :return: None
    """

    await user_service.create_order(message)
    logger.info("Order %s successfully created", message)


@rabbit_router.subscriber(
    queue=update_order_queue_init,
    exchange=update_order_exch_init,
)
async def update_order(
    message: Order,
    user_service: UserServiceDep,
) -> None:
    """
    Update existing order in storage from the message payload.

    :param message: Order with fields to apply
    :param user_service: Injected user service
    :return: None
    """

    order = await user_service.edit_order(message)
    logger.info("Order %s successfully updated", order)


@rabbit_router.subscriber(
    queue=cancel_order_queue_init,
    exchange=cancel_order_exch_init,
)
async def cancel_order(message: Order, user_service: UserServiceDep) -> None:
    """
    Cancel (delete) an order identified by the message.

    :param message: Order reference (e.g. id) for cancellation
    :param user_service: Injected user service
    :return: None
    """

    await user_service.cancel_order(message)
    logger.info("Order %s successfully deleted", message)


@rabbit_router.subscriber(
    queue=get_orders_queue_init,
    exchange=get_orders_into_exch_init,
)
async def get_orders(
    message: Order,
    user_service: UserServiceDep,
) -> None:
    """
    Load all orders for the user id carried in the message (async reply path in service).

    :param message: Order-shaped message with user_id set
    :param user_service: Injected user service
    :return: None
    """

    await user_service.get_orders_list(message)
    logger.info("Order for user %s successfully retrieved", message.user_id)


@rabbit_router.subscriber(
    queue=get_order_queue_init,
    exchange=get_order_into_exch_init,
)
async def get_order(
    message: Order,
    user_service: UserServiceDep,
) -> None:
    """
    Load a single order by id from the message.

    :param message: Order with id to fetch
    :param user_service: Injected user service
    :return: None
    """

    await user_service.get_order(message)
    logger.info("Order for user %s successfully retrieved", message.user_id)
