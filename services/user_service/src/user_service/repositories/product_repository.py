from sqlalchemy.ext.asyncio import AsyncSession

from common.persistence import BaseRepository
from common.persistence.models import Product


class ProductsRepository(BaseRepository[Product]):
    """Product Repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Init Product Repository."""

        super().__init__(session, Product)
