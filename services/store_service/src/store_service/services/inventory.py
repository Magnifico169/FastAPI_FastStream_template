import logging
from typing import Annotated

from fastapi import Depends

from common.domain import Product
from store_service.repositories import (
    ProductsRepository,
    ProductsRepositoryDependence,
)

logger = logging.getLogger(__name__)


class InventoryService:
    """
    Inventory Service class.
    """

    def __init__(self, product_repository: ProductsRepository) -> None:
        """
        Initializes the Inventory_service service.

        :param product_repository: Product repository
        :return: None
        """
        self.product_repository = product_repository

    async def add_product_to_inventory(self, product: Product) -> Product:
        """
        Add product to inventory: create row or increase count for matching name/price/created_at.

        :param product: Product to add or merge
        :return: Persisted product row after create or count update
        """
        inventory_product = await self.product_repository.filter_by(
            **{
                "name": product.name,
                "price": product.price,
                "created_at": product.created_at,
            }
        )

        if not inventory_product:
            return await self.product_repository.create(product)
        inventory_product[0].count += product.count
        return await self.product_repository.update(inventory_product[0], inventory_product)

    async def update_product_inventory(self, product: Product) -> Product:
        """
        Update matching inventory row, or create if no row matches the identity fields.

        :param product: New field values; missing row triggers create and warning
        :return: Persisted product after update or create
        """
        inventory_product = await self.product_repository.filter_by(
            **{
                "name": product.name,
                "price": product.price,
                "created_at": product.created_at,
            }
        )
        if not inventory_product:
            logger.warning("Product %s not found.", product.name)
            return await self.product_repository.create(product)
        return await self.product_repository.update(product, inventory_product[0])

    async def remove_product_from_inventory(self, product: Product) -> None:
        """
        Remove product from inventory by id; logs a warning if id was not found.

        :param product: Product with id to delete
        :return: None
        """
        is_delete = await self.product_repository.delete(product.id)
        if not is_delete:
            logger.warning("Product %s not found.", product.name)
        return None


def get_inventory_service(
    product_repository: ProductsRepositoryDependence,
) -> InventoryService:
    """Get Inventory Service class."""
    return InventoryService(product_repository)


InventoryServiceDep = Annotated[InventoryService, Depends(get_inventory_service)]
