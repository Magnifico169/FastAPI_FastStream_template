from sqlalchemy.ext.asyncio import AsyncSession

from common.persistence import BaseRepository
from common.persistence.models import User


class UsersRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)
