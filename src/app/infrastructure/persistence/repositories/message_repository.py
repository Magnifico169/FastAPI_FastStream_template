from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.persistence import MessagePersistenceError
from app.domain.models.message import Message
from app.infrastructure.persistence.models.message import MessageORM


class MessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, message: Message) -> Message:
        orm = MessageORM(
            text=message.text,
            status=message.status.value,
        )
        try:
            self._session.add(orm)
            await self._session.commit()
            await self._session.refresh(orm)
        except SQLAlchemyError as err:
            await self._session.rollback()
            raise MessagePersistenceError(str(err)) from err
        return Message.model_validate(orm)
