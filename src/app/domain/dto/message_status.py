from pydantic import BaseModel

from app.domain.enums.message_status import MessageStatus


class MessageStatusResponseDTO(BaseModel):
    status: MessageStatus
