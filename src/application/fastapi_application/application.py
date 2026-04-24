from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.order_routes import order_router
from api.v1.user_routes import user_router
from core.models.rabbit.rabbit import rabbit_broker, rabbit_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with rabbit_broker.lifespan_context(application):
        yield


app = FastAPI(
    title="Order service",
    description="Retrieve context from Confluence and Materials DB for RAG pipeline",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, tags=["User"])
app.include_router(order_router, tags=["Order"])
app.include_router(rabbit_router)
