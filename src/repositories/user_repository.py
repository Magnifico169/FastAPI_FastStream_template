from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.models.db.users import User


class UsersRepository(BaseRepository[User]):
    """
    Repository for users
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)
