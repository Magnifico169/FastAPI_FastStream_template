from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.models.db.products import Product


class ProductsRepository(BaseRepository[Product]):
    """
    Repository for products
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)
