from user_service.repositories.dependencies import (
    OrdersRepositoryDependence,
    ProductsRepositoryDependence,
    UsersRepositoryDependence,
    get_order_repository,
    get_product_repository,
    get_user_repository,
)
from user_service.repositories.order_repository import OrdersRepository
from user_service.repositories.product_repository import ProductsRepository
from user_service.repositories.user_repository import UsersRepository

__all__ = [
    "OrdersRepository",
    "OrdersRepositoryDependence",
    "ProductsRepository",
    "ProductsRepositoryDependence",
    "UsersRepository",
    "UsersRepositoryDependence",
    "get_order_repository",
    "get_product_repository",
    "get_user_repository",
]
