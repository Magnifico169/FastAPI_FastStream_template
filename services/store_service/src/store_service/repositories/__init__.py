from store_service.repositories.dependencies import (
    ProductsRepositoryDependence,
    get_product_repository,
)
from store_service.repositories.product_repository import ProductsRepository

__all__ = [
    "ProductsRepository",
    "ProductsRepositoryDependence",
    "get_product_repository",
]
