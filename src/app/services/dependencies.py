from typing import Annotated

from fastapi import Depends

from app.infrastructure.persistence.repositories.message_repository import MessageRepository
from app.infrastructure.persistence.session import AsyncSessionDep
from app.services.message_service import MessageService


def get_message_repository(session: AsyncSessionDep) -> MessageRepository:
    return MessageRepository(session)


def get_message_service(
    repository: Annotated[MessageRepository, Depends(get_message_repository)],
) -> MessageService:
    return MessageService(repository=repository)


MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
