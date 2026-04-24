from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    FAILED = "FAILED"


class OrderStatusRequestSchema(BaseModel):
    """
    Order Status Request model

    :ivar order_id: Order ID
    :ivar user_id: User ID
    """

    order_id: UUID = Field(..., description="Order ID")
    user_id: UUID = Field(..., description="User ID")


class OrderStatusResponseSchema(BaseModel):
    """
    Order Status Response model

    :ivar order_id: Order ID
    :ivar user_id: User ID
    :ivar status: Order Status
    """

    order_id: UUID = Field(..., description="Order ID")
    user_id: UUID = Field(..., description="User ID")
    status: OrderStatus = Field(..., description="Order Status")
