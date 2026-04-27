from fastapi import APIRouter, status

from common.messaging import (
    create_user_exch_init,
    create_user_queue_init,
    rabbit_broker,
)
from common.schemas import MessageStatusResponse, UserInfoSchema
from common.constants import MessageStatus

user_router = APIRouter()


@user_router.post(
    "/user",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MessageStatusResponse,
    tags=["user"],
)
async def create_user(message: UserInfoSchema) -> MessageStatusResponse:
    await rabbit_broker.publish(
        message,
        queue=create_user_queue_init,
        exchange=create_user_exch_init,
    )
    return MessageStatusResponse(message=MessageStatus.PROCESSING)
