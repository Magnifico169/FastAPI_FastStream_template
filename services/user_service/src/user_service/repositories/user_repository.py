from sqlalchemy.ext.asyncio import AsyncSession

from common.persistence import BaseRepository
from common.persistence.models import User


class UsersRepository(BaseRepository[User]):
    """User Repository."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Init UsersRepository.

        :param session: Async SQLAlchemy session for this request scope
        :return: None
        """

        super().__init__(session, User)
