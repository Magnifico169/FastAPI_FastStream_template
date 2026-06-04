from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.message_status import MessageStatus


class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID | None = Field(default=uuid4(), description="Message ID")
    text: str = Field(..., description="Message text")
    status: MessageStatus = Field(..., description="Message status")
    created_at: datetime | None = Field(default=None, description="Message created at")
