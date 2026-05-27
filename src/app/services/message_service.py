from app.domain.dto.message_create import MessageCreateDTO
from app.domain.enums.message_status import MessageStatus
from app.domain.exceptions.broker import BrokerPublishError
from app.domain.models.message import Message
from app.infrastructure.messaging.rabbit import messages_exchange, messages_queue, rabbit_broker
from app.infrastructure.persistence.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, repository: MessageRepository) -> None:
        self._repository = repository

    async def enqueue(self, dto: MessageCreateDTO) -> None:
        message = Message(text=dto.text, status=MessageStatus.PROCESSING)
        try:
            await rabbit_broker.publish(
                message,
                queue=messages_queue,
                exchange=messages_exchange,
            )
        except (ConnectionError, OSError, RuntimeError) as err:
            raise BrokerPublishError(str(err)) from err

    async def process(self, message: Message) -> Message:
        message.status = MessageStatus.PROCESSED
        return await self._repository.create(message)
