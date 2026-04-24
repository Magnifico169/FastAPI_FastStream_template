from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.models.db.products import Products


class ProductRepository(BaseRepository):
    """
    Repository for products
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, Products)
