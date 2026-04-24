from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.models.db.orders import Orders


class OrderRepository(BaseRepository):
    """
    Repository for orders
    """
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Orders)
