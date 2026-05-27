from fastapi import APIRouter, status

from app.domain.dto.message_create import MessageCreateDTO
from app.domain.dto.message_status import MessageStatusResponseDTO
from app.domain.enums.message_status import MessageStatus
from app.services.dependencies import MessageServiceDep

messages_router = APIRouter()


@messages_router.post(
    "/messages",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["messages"],
)
async def create_message(
    message: MessageCreateDTO,
    message_service: MessageServiceDep,
) -> MessageStatusResponseDTO:
    await message_service.enqueue(message)
    return MessageStatusResponseDTO(status=MessageStatus.PROCESSING)
