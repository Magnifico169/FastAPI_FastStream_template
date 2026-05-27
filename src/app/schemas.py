from enum import StrEnum

from pydantic import BaseModel, Field


class MessageStatus(StrEnum):
    PROCESSING = "processing"


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, examples=["hello"])


class MessageStatusResponse(BaseModel):
    status: MessageStatus
