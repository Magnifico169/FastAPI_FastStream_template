from typing import Annotated

from fastapi import Depends

from user_service.repositories.order_repository import OrdersRepository
from user_service.repositories.product_repository import ProductsRepository
from user_service.repositories.user_repository import UsersRepository
from common.persistence import AsyncSessionDep


def get_order_repository(session: AsyncSessionDep) -> OrdersRepository:
    """Get Orders Repository."""
    return OrdersRepository(session)


def get_user_repository(session: AsyncSessionDep) -> UsersRepository:
    """Get Users Repository."""
    return UsersRepository(session)


def get_product_repository(session: AsyncSessionDep) -> ProductsRepository:
    """Get Products Repository."""
    return ProductsRepository(session)


OrdersRepositoryDependence = Annotated[OrdersRepository, Depends(get_order_repository)]
UsersRepositoryDependence = Annotated[UsersRepository, Depends(get_user_repository)]
ProductsRepositoryDependence = Annotated[ProductsRepository, Depends(get_product_repository)]
