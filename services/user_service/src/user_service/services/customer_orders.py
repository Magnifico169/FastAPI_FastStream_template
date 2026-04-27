import logging
from typing import Annotated

from fastapi import Depends

from common.domain import Order
from user_service.repositories import (
    OrdersRepository,
    OrdersRepositoryDependence,
    ProductsRepository,
    ProductsRepositoryDependence,
)

logger = logging.getLogger(__name__)


class UserService:
    """User Service."""

    def __init__(
        self,
        products_repository: ProductsRepository,
        order_repository: OrdersRepository,
    ) -> None:
        """
        Init UserService.

        :param products_repository: ProductsRepositoryDependence
        :param order_repository: OrdersRepositoryDependence
        :return: None
        """
        self.products_repository = products_repository
        self.order_repository = order_repository

    async def create_order(self, order: Order) -> Order | None:
        """
        Create new order.

        :param order:
        :return:
        """
        for product in order.products:
            inventory_product = await self.products_repository.filter_by(
                **{
                    "name": product.name,
                    "price": product.price,
                    "created_at": product.created_at,
                }
            )
            if not inventory_product:
                logger.warning("Product %s not found.", product.name)
                continue
            if inventory_product[0].count - product.count > 0:
                inventory_product[0].count -= product.count
            else:
                logger.error("Product %s is out of stock", inventory_product[0].name)
                return None
            await self.products_repository.update(inventory_product[0], inventory_product)

        return await self.order_repository.create(order)

    async def edit_order(self, order: Order) -> Order | None:
        """
        Edit existing order.

        :param order:
        :return:
        """
        existing_order = await self.order_repository.get(order.id)
        if not existing_order:
            logger.warning("Order %s not found.", order.id)
            return None
        return await self.order_repository.update(existing_order, order)

    async def cancel_order(self, order: Order) -> None:
        """
        Cancel existing order.

        :param order:
        :return:
        """
        is_delete = await self.order_repository.delete(order.id)
        if not is_delete:
            logger.warning("Failed to delete order %s.", order.id)
        return None

    async def get_orders_list(self, message: Order) -> list[Order] | None:
        """
        Get list of orders.

        :param message:
        :return:
        """
        orders = await self.order_repository.filter_by(**{"user_id": message.user_id})
        if not orders:
            logger.error("Order %s not found", message.user_id)
            return

    async def get_order(self, message: Order) -> Order | None:
        """
        Get order by id.

        :param message:
        :return:
        """
        order = await self.order_repository.get(message.id)
        if not order:
            logger.error("Order %s not found", message.id)
            return None
        return order


def get_user_service(
    products_repository: ProductsRepositoryDependence,
    order_repository: OrdersRepositoryDependence,
) -> UserService:
    """Get User Service."""
    return UserService(products_repository, order_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
