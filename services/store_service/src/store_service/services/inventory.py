import logging
from typing import Annotated

from fast_depends import Depends

from common.domain import Product
from store_service.repositories import (
    ProductsRepository,
    ProductsRepositoryDependence,
)

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self, product_repository: ProductsRepository) -> None:
        self.product_repository = product_repository

    async def add_product_to_inventory(self, product: Product) -> Product:
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
        is_delete = await self.product_repository.delete(product.id)
        if not is_delete:
            logger.warning("Product %s not found.", product.name)
        return None


def get_inventory_service(
    product_repository: ProductsRepositoryDependence,
) -> InventoryService:
    return InventoryService(product_repository)


InventoryServiceDep = Annotated[InventoryService, Depends(get_inventory_service)]
