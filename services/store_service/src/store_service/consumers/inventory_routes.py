import logging

from common.domain import Product
from common.messaging import (
    create_product_exch_init,
    create_product_queue_init,
    delete_product_exch_init,
    delete_product_queue_init,
    rabbit_router,
    update_product_exch_init,
    update_product_queue_init,
)
from store_service.services import InventoryServiceDep

logger = logging.getLogger(__name__)


@rabbit_router.subscriber(
    queue=create_product_queue_init,
    exchange=create_product_exch_init,
)
async def create_product(
    message: Product,
    inventory_service: InventoryServiceDep,
) -> None:
    """
    Create a new user.

    :param inventory_service:
    :param message:
    :return: None
    """
    await inventory_service.add_product_to_inventory(message)
    logger.info("Product %s successfully created", message)


@rabbit_router.subscriber(
    queue=update_product_queue_init,
    exchange=update_product_exch_init,
)
async def update_product(
    message: Product,
    inventory_service: InventoryServiceDep,
) -> None:
    """
    Update an existing order.

    :param message:
    :param inventory_service:
    :return:
    """
    await inventory_service.update_product_inventory(message)
    logger.info("Product %s successfully updated", message)


@rabbit_router.subscriber(
    queue=delete_product_queue_init,
    exchange=delete_product_exch_init,
)
async def delete_product(
    message: Product,
    inventory_service: InventoryServiceDep,
) -> None:
    """
    Delete an existing product.

    :param message:
    :param inventory_service:
    :return:
    """
    await inventory_service.remove_product_from_inventory(message)
    logger.info("Product %s successfully deleted", message)
