import logging

from app.messaging import messages_exchange, messages_queue, rabbit_router
from app.schemas import MessageCreate

logger = logging.getLogger(__name__)


@rabbit_router.subscriber(
    queue=messages_queue,
    exchange=messages_exchange,
)
async def handle_message(message: MessageCreate) -> None:
    """Process a message received from RabbitMQ."""

    logger.info("Received message: %s", message.text)
