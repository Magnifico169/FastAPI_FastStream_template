from pydantic import BaseModel, Field

from common.constants.message_status import MessageStatus


class MessageStatusResponse(BaseModel):
    """
    Message status response

    :ivar message: message status
    :vartype message: MessageStatus
    :ivar status: message status
    :vartype status: MessageStatus
    """

    message: MessageStatus = Field(..., description="The status of the message.")
    status: int = Field(default=202, ge=100, le=599)
