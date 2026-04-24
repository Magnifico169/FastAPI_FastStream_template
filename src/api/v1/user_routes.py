from fastapi import APIRouter, status

from infrastructure.rabbit import (
    create_user_exch_init,
    create_user_queue_init,
    rabbit_broker,
)
from models.schemas.response import MessageStatusResponse
from models.schemas import UserInfoSchema

user_router = APIRouter()


@user_router.post(
    "/user",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=MessageStatusResponse,
    tags=["user"],
)
async def create_user(body: UserInfoSchema) -> MessageStatusResponse:
    await rabbit_broker.publish(
        body,
        queue=create_user_queue_init,
        exchange=create_user_exch_init,
    )
    return MessageStatusResponse(
        message="processing",
        status=status.HTTP_202_ACCEPTED,
    )
