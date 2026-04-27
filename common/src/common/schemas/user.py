from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.user_status import UserStatus


class UserInfoSchema(BaseModel):
    user_id: UUID = Field(..., description="User ID")
    nickname: str = Field(..., description="Public or internal display name for the user.")
    delivery_address: str = Field(..., description="Default shipping or hand-off address.")
    status: UserStatus = Field(..., description="User status")
