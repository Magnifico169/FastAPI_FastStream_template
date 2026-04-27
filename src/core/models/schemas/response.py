from pydantic import BaseModel, Field
from fastapi import status

from constants.message_status import MessageStatus


class MessageStatusResponse(BaseModel):
    """
    Message Status Response model

    :ivar message: Message Status
    :vartype message: MessageStatus
    :ivar status: FastAPI status code
    :vartype status: int
    """

    message: MessageStatus = Field(..., description="The status of the message.")
    status: int = Field(default=status.HTTP_202_ACCEPTED, ge=100, le=599)
