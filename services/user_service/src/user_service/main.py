import asyncio
from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.persistence import PostgresSessionFactory
from common.messaging import rabbit_broker, rabbit_router
from user_service.api.v1.order_routes import order_router
from user_service.api.v1.user_routes import user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager."""

    await PostgresSessionFactory.initialize()
    try:
        await rabbit_broker.start()
    except ConnectionError as err:
        logger.error("Connection error during start application: %s", err)
        raise err

    yield

    try:
        await rabbit_broker.stop()
    except ConnectionError as err:
        logger.error("Connection error during stop application: %s", err)
        raise err
    await PostgresSessionFactory.close()


app = FastAPI(
    title="User service (customer API)",
    description="HTTP gateway for end-user registration and order commands",
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

app.include_router(user_router)
app.include_router(order_router)
app.include_router(rabbit_router)


async def run() -> None:
    """Run the FastAPI application."""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
