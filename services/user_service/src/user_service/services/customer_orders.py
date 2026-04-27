import logging
from typing import Annotated

from fastapi import Depends

from common.domain import Order
from common.utils.pydantic_db import json_fields, model_dump_for_orm
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

        :param products_repository: Store inventory product rows (stock)
        :param order_repository: Order persistence
        :return: None
        """
        self.products_repository = products_repository
        self.order_repository = order_repository

    async def create_order(self, order: Order) -> Order | None:
        """
        Reserve stock for each line and insert the order; skips missing products, aborts on stock.

        :param order: Order with product lines
        :return: Created order model, or None if any line is out of stock
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

        row = model_dump_for_orm(
            order,
            exclude_unset=False,
            json_fields=json_fields,
        )
        return await self.order_repository.create(row)

    async def edit_order(self, order: Order) -> Order | None:
        """
        Replace an existing order’s fields with the given payload (partial update via model_dump).

        :param order: Order id and new values
        :return: Updated order model, or None if the order id was not found
        """
        existing_order = await self.order_repository.get(order.id)
        if not existing_order:
            logger.warning("Order %s not found.", order.id)
            return None
        row = model_dump_for_orm(
            order,
            exclude_unset=True,
            json_fields=json_fields,
        )
        return await self.order_repository.update(existing_order, row)

    async def cancel_order(self, order: Order) -> None:
        """
        Delete an order by id; logs a warning if the row did not exist.

        :param order: Order whose id to delete
        :return: None
        """
        is_delete = await self.order_repository.delete(order.id)
        if not is_delete:
            logger.warning("Failed to delete order %s.", order.id)
        return None

    async def get_orders_list(self, message: Order) -> list[Order] | None:
        """
        Load orders for message.user_id from storage.

        :param message: Carries user_id to filter
        :return: List of orders for that user, or None if no rows (also logs on empty)
        """
        orders = await self.order_repository.filter_by(**{"user_id": message.user_id})
        if not orders:
            logger.error("Order %s not found", message.user_id)
            return

    async def get_order(self, message: Order) -> Order | None:
        """
        Fetch a single order by message.id.

        :param message: Order with id to load
        :return: Order row, or None if not found
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
