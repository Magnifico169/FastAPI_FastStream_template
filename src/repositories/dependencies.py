from fast_depends import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository


def get_order_repository(session: AsyncSession) -> OrderRepository:
    """
    Get the order repository.

    :returns: The order repository.
    """
    return OrderRepository(session)

def get_user_repository(session: AsyncSession) -> UserRepository:
    """
    Get the user repository.

    :returns: The user repository.
    """
    return UserRepository(session)

def get_product_repository(session: AsyncSession) -> ProductRepository:
    """
    Get the product repository.

    :returns: The product repository.
    """
    return ProductRepository(session)


OrdersRepositoryDependence = Annotated[OrderRepository, Depends(get_order_repository)]
UserRepositoryDependence = Annotated[UserRepository, Depends(get_user_repository)]
ProductRepositoryDependence = Annotated[ProductRepository, Depends(get_product_repository)]