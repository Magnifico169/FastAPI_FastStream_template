from typing import Annotated

from fastapi import Depends

from store_service.repositories.product_repository import ProductsRepository
from common.persistence import AsyncSessionDep


def get_product_repository(session: AsyncSessionDep) -> ProductsRepository:
    """Get Product Repository class."""

    return ProductsRepository(session)


ProductsRepositoryDependence = Annotated[ProductsRepository, Depends(get_product_repository)]
