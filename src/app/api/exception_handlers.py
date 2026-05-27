from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.base import AppError
from app.domain.exceptions.broker import BrokerPublishError


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message, "code": exc.code},
    )


async def broker_publish_error_handler(_request: Request, exc: BrokerPublishError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": exc.message, "code": exc.code},
    )


def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(AppError, app_error_handler)
    application.add_exception_handler(BrokerPublishError, broker_publish_error_handler)
