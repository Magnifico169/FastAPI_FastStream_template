from sqlalchemy.ext.asyncio import AsyncSession

from common.persistence import BaseRepository
from common.persistence.models import Order


class OrdersRepository(BaseRepository[Order]):
    """Orders Repository."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Init Orders Repository.

        :param session: Async SQLAlchemy session for this request scope
        :return: None
        """

        super().__init__(session, Order)
