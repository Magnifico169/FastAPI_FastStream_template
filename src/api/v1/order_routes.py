from fastapi import APIRouter

order_router = APIRouter()


@order_router.get("/order_status", tags=["order"])
async def get_order_status():
    pass


@order_router.post("/order", tags=["order"])
async def create_order():
    pass


@order_router.delete("/order", tags=["order"])
async def delete_order():
    pass


@order_router.put("/order", tags=["order"])
async def update_order():
    pass


@order_router.get("/orders_status", tags=["order"])
async def get_orders_status():
    pass
