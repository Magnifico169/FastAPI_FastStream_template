from fast_depends import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from repositories.order_repository import OrdersRepository
from repositories.product_repository import ProductsRepository
from repositories.user_repository import UsersRepository


def get_order_repository(session: AsyncSession) -> OrdersRepository:
    """
    Get the order repository.

    :returns: The order repository.
    """
    return OrdersRepository(session)


def get_user_repository(session: AsyncSession) -> UsersRepository:
    """
    Get the user repository.

    :returns: The user repository.
    """
    return UsersRepository(session)


def get_product_repository(session: AsyncSession) -> ProductsRepository:
    """
    Get the product repository.

    :returns: The product repository.
    """
    return ProductsRepository(session)


OrdersRepositoryDependence = Annotated[OrdersRepository, Depends(get_order_repository)]
UsersRepositoryDependence = Annotated[UsersRepository, Depends(get_user_repository)]
ProductsRepositoryDependence = Annotated[ProductsRepository, Depends(get_product_repository)]
