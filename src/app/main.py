import asyncio
from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.v1.messages import messages_router
from app.consumers import message_handler  # noqa: F401
from app.infrastructure.messaging.rabbit import rabbit_broker, rabbit_router
from app.infrastructure.persistence.session import PostgresSessionFactory

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    try:
        await PostgresSessionFactory.initialize()
        await rabbit_broker.start()
    except (ConnectionError, OSError, RuntimeError) as err:
        logger.exception("Error during application start")
        raise err from None

    yield

    try:
        await rabbit_broker.stop()
        await PostgresSessionFactory.close()
    except (ConnectionError, OSError, RuntimeError) as err:
        logger.exception("Error during application stop")
        raise err from None


def create_app() -> FastAPI:
    application = FastAPI(
        title="FastStream Template",
        description="FastAPI + FastStream (RabbitMQ) with Postgres persistence",
        version="0.1.0",
        lifespan=lifespan,
    )

    register_exception_handlers(application)
    application.include_router(messages_router)
    application.include_router(rabbit_router)

    @application.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()


async def run() -> None:
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
