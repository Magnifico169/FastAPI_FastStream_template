from pydantic import BaseModel, Field

from common.constants.message_status import MessageStatus


class MessageStatusResponse(BaseModel):
    message: MessageStatus = Field(..., description="The status of the message.")
    status: int = Field(default=202, ge=100, le=599)
