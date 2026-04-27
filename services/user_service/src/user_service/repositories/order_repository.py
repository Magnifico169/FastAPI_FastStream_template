from sqlalchemy.ext.asyncio import AsyncSession

from common.persistence import BaseRepository
from common.persistence.models import Order


class OrdersRepository(BaseRepository[Order]):
    """Orders Repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init Orders Repository."""

        super().__init__(session, Order)
