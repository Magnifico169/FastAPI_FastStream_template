from sqlalchemy.ext.asyncio import AsyncSession

from common.persistence import BaseRepository
from common.persistence.models import Product


class ProductsRepository(BaseRepository[Product]):
    """Product Repository class."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Init Product Repository class.

        :param session: Async SQLAlchemy session for this request scope
        :return: None
        """
        super().__init__(session, Product)
