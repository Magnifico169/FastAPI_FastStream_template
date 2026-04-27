import logging

from infrastructure.rabbit.rabbit import (
    rabbit_broker,
    create_user_queue_init,
    create_user_exch_init,
    create_order_exch_init,
    create_order_queue_init,
    update_order_exch_init,
    update_order_queue_init,
    cancel_order_exch_init,
    cancel_order_queue_init,
    get_orders_into_exch_init,
    get_orders_queue_init,
    get_order_into_exch_init,
    get_order_queue_init,
    create_product_exch_init,
    create_product_queue_init,
    delete_product_exch_init,
    delete_product_queue_init,
    update_product_exch_init,
    update_product_queue_init,
)
from core.models.domain import Order, Product, User
from services import ShopServiceDep, UserServiceDep


logger = logging.getLogger(__name__)


@rabbit_broker.subscriber(
    queue=create_user_queue_init,
    exchange=create_user_exch_init,
)
async def create_user(message: User, shop_service: ShopServiceDep) -> None:
    """
    Create a new user.

    :param shop_service:
    :param message:
    :return: None
    """
    await shop_service.create_user(message)
    logger.info("User %s successfully created", message)


@rabbit_broker.subscriber(
    queue=create_order_queue_init,
    exchange=create_order_exch_init,
)
async def create_order(message: Order, user_service: UserServiceDep) -> None:
    """
    Create a new order.

    :param message:
    :param user_service:
    :return: None
    """
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
    """
    Update an existing order.

    :param message:
    :param user_service:
    :return:
    """
    order = await user_service.edit_order(message)
    logger.info("Order %s successfully updated", order)


@rabbit_broker.subscriber(
    queue=cancel_order_queue_init,
    exchange=cancel_order_exch_init,
)
async def cancel_order(message: Order, user_service: UserServiceDep) -> None:
    """
    Delete an existing order.

    :param message:
    :param user_service:
    :return:
    """
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
    """
    Get all orders.

    :param message:
    :param user_service:
    :return:
    """
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
    """
    Get an existing order.

    :param message:
    :param user_service:
    :return: None
    """
    await user_service.get_order(message)
    logger.info("Order for user %s successfully retrieved", message.user_id)


@rabbit_broker.subscriber(
    queue=create_product_queue_init,
    exchange=create_product_exch_init,
)
async def create_product(
    message: Product,
    inventory_service: ShopServiceDep,
) -> None:
    """
    Create a new product.

    :param message:
    :param inventory_service:
    :return:
    """
    await inventory_service.add_product_to_inventory(message)
    logger.info("Product %s successfully created", message)


@rabbit_broker.subscriber(
    queue=update_product_queue_init,
    exchange=update_product_exch_init,
)
async def update_product(
    message: Product,
    inventory_service: ShopServiceDep,
) -> None:
    """
    Update an existing product.

    :param message:
    :param inventory_service:
    :return:
    """
    await inventory_service.update_product_inventory(message)
    logger.info("Product %s successfully updated", message)


@rabbit_broker.subscriber(
    queue=delete_product_queue_init,
    exchange=delete_product_exch_init,
)
async def delete_product(
    message: Product,
    inventory_service: ShopServiceDep,
) -> None:
    """
    Delete an existing product.

    :param message:
    :param inventory_service:
    :return:
    """
    await inventory_service.remove_product_from_inventory(message)
    logger.info("Product %s successfully deleted", message)
