from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.infrastructure.settings.postgres import get_postgres_settings


class PostgresSessionFactory:
    _engine = None
    _session_maker: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    async def initialize(cls) -> None:
        settings = get_postgres_settings()
        cls._engine = create_async_engine(
            settings.get_database_url(),
            pool_size=settings.POSTGRES_POOL_SIZE,
            max_overflow=settings.POSTGRES_MAX_OVERFLOW,
            pool_pre_ping=settings.POSTGRES_POOL_PRE_PING,
            pool_recycle=settings.POSTGRES_POOL_RECYCLE,
        )
        cls._session_maker = async_sessionmaker(cls._engine, expire_on_commit=False)

    @classmethod
    async def close(cls) -> None:
        if cls._engine is not None:
            await cls._engine.dispose()
            cls._engine = None
            cls._session_maker = None

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        if cls._session_maker is None:
            msg = "Database session factory is not initialized"
            raise RuntimeError(msg)
        async with cls._session_maker() as session:
            yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(PostgresSessionFactory.get_session)]
