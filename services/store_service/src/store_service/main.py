import asyncio
from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.persistence import PostgresSessionFactory
from common.messaging import rabbit_router, rabbit_broker
from store_service.api.v1.inventory_routes import inventory_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  #noqa:ARG001
    """Lifespan context manager."""

    await PostgresSessionFactory.initialize()
    try:
        await rabbit_broker.start()
    except ConnectionError as err:
        logger.exception("Connection error during start application: %s",)
        raise err from None

    yield

    try:
        await rabbit_broker.stop()
    except ConnectionError as err:
        logger.exception("Connection error during stop application: %s",)
        raise err from None
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

app.include_router(inventory_router)
app.include_router(rabbit_router)


async def run() -> None:
    """Run the application."""
    config = uvicorn.Config(app, host="0.0.0.0", port=8001)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
