import logging
from typing import Annotated

from fast_depends import Depends

from models.domain import Product, User
from repositories import (
    UsersRepository,
    UsersRepositoryDependence,
    ProductsRepository,
    ProductsRepositoryDependence,
)

logger = logging.getLogger(__name__)


class ShopService:
    """
    Shop Service
    """

    def __init__(
        self,
        user_repository: UsersRepository,
        product_repository: ProductsRepository,
    ) -> None:
        """
        Initializes the Shop service.

        :param user_repository: User repository
        :param product_repository: Product repository
        :return None
        """
        self.user_repository = user_repository
        self.product_repository = product_repository

    async def create_user(self, user: User) -> User:
        """
        Create a new user.

        :param user:
        :return:
        """
        return await self.user_repository.create(user)

    async def add_product_to_inventory(self, product: Product) -> Product:
        """
        Add product to inventory.

        :param product:
        :return:
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
        else:
            inventory_product.count += product.count
            return await self.product_repository.update(inventory_product[0], inventory_product)

    async def update_product_inventory(self, product: Product) -> Product:
        """
        Update product inventory.

        :param product:
        :return:
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
        Remove product from inventory.

        :param product:
        :return:
        """

        is_delete = await self.product_repository.delete(product.id)
        if not is_delete:
            logger.warning("Product %s not found.", product.name)
            return None
        return None


def get_inventory_service(
    user_repository: UsersRepositoryDependence,
    product_repository: ProductsRepositoryDependence,
) -> ShopService:
    return ShopService(user_repository, product_repository)


ShopServiceDep = Annotated[ShopService, Depends(get_inventory_service)]
