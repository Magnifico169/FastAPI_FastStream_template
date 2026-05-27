import logging

from app.domain.models.message import Message
from app.infrastructure.messaging.rabbit import messages_exchange, messages_queue, rabbit_router
from app.services.dependencies import MessageServiceDep

logger = logging.getLogger(__name__)


@rabbit_router.subscriber(
    queue=messages_queue,
    exchange=messages_exchange,
)
async def handle_message(
    message: Message,
    message_service: MessageServiceDep,
) -> None:
    saved = await message_service.process(message)
    logger.info("Message processed and saved: id=%s text=%s", saved.id, saved.text)
