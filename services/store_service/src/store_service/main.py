import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.messaging import rabbit_broker, rabbit_router
from store_service.api.v1.inventory_routes import inventory_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    from common.persistence import PostgresSessionFactory

    PostgresSessionFactory.initialize()
    try:
        async with rabbit_broker.lifespan_context(application):
            yield
    finally:
        await PostgresSessionFactory.close()


app = FastAPI(
    title="Store service (catalog / inventory API)",
    description="HTTP gateway for product and inventory management",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router, tags=["Inventory"])
app.include_router(rabbit_router)


async def run() -> None:
    config = uvicorn.Config(app, host="0.0.0.0", port=8001)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
