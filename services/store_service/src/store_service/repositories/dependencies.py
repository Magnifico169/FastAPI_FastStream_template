from typing import Annotated

from fast_depends import Depends

from store_service.repositories.product_repository import ProductsRepository
from common.persistence import AsyncSessionDep


def get_product_repository(session: AsyncSessionDep) -> ProductsRepository:
    return ProductsRepository(session)


ProductsRepositoryDependence = Annotated[ProductsRepository, Depends(get_product_repository)]
