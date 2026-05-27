from fastapi import APIRouter, status

from app.messaging import messages_exchange, messages_queue, rabbit_broker
from app.schemas import MessageCreate, MessageStatus, MessageStatusResponse

api_router = APIRouter()


@api_router.post(
    "/messages",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["messages"],
)
async def create_message(message: MessageCreate) -> MessageStatusResponse:
    """Accept a message and publish it to RabbitMQ for async processing."""

    await rabbit_broker.publish(
        message,
        queue=messages_queue,
        exchange=messages_exchange,
    )
    return MessageStatusResponse(status=MessageStatus.PROCESSING)
