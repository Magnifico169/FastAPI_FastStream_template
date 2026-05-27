import asyncio
from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI

from app.consumers import handler  # noqa: F401 — register subscribers
from app.api.routes import api_router
from app.messaging import rabbit_broker, rabbit_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    try:
        await rabbit_broker.start()
    except ConnectionError as err:
        logger.exception("Connection error during application start")
        raise err from None

    yield

    try:
        await rabbit_broker.stop()
    except ConnectionError as err:
        logger.exception("Connection error during application stop")
        raise err from None


app = FastAPI(
    title="FastStream Template",
    description="Minimal FastAPI + FastStream (RabbitMQ) example",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)
app.include_router(rabbit_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


async def run() -> None:
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
