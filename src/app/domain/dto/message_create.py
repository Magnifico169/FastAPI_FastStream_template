from pydantic import BaseModel, Field


class MessageCreateDTO(BaseModel):
    text: str = Field(min_length=1, examples=["hello"])
