from pydantic import BaseModel, Field

from constants.message_status import MessageStatus


class MessageStatusResponse(BaseModel):
    message: MessageStatus = Field(..., description="The status of the message.")
    status: int = Field(..., ge=100, le=599)
