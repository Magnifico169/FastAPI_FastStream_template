from fastapi import APIRouter

user_router = APIRouter()


@user_router.post("/user", tags=["user"])
async def create_user():
    pass


@user_router.delete("/user", tags=["user"])
async def delete_user():
    pass
