from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.user_status import UserStatus


class UserInfoSchema(BaseModel):
    """
    User info schema

    :ivar user_id: User ID
    :vartype user_id: UUID
    :ivar nickname: User nickname
    :vartype nickname: String
    :ivar delivery_address: User delivery address
    :vartype delivery_address: String
    :ivar status: User status
    :vartype status: String
    """

    user_id: UUID = Field(..., description="User ID")
    nickname: str = Field(..., description="Public or internal display name for the user.")
    delivery_address: str = Field(..., description="Default shipping or hand-off address.")
    status: UserStatus = Field(..., description="User status")
