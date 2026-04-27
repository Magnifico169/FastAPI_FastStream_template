from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from typing import Annotated, ClassVar

from fast_depends import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from common.settings import get_postgres_settings


class PostgresSessionFactory:
    _session_factory: ClassVar[async_sessionmaker[AsyncSession] | None] = None

    @classmethod
    def initialize(cls) -> None:
        postgres_settings = get_postgres_settings()
        if cls._session_factory is not None:
            raise RuntimeError("Session factory already initialized")

        async_driver = postgres_settings.POSTGRES_DRIVER
        database_url = postgres_settings.get_postgres_uri().replace(
            postgres_settings.POSTGRES_DRIVER,
            async_driver,
        )

        engine = create_async_engine(
            database_url,
            pool_size=postgres_settings.POSTGRES_POOL_SIZE,
            max_overflow=postgres_settings.POSTGRES_MAX_OVERFLOW,
            pool_pre_ping=postgres_settings.POSTGRES_POOL_PRE_PING,
            pool_recycle=postgres_settings.POSTGRES_POOL_RECYCLE,
        )

        cls._session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @classmethod
    @asynccontextmanager
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        if cls._session_factory is None:
            raise RuntimeError("Session factory not initialized. Call initialize() first.")

        session = cls._session_factory()
        try:
            yield session
        finally:
            await session.close()

    @classmethod
    async def close(cls) -> None:
        if cls._session_factory is not None:
            bind = getattr(cls._session_factory, "bind", None)
            if bind is None:
                bind = cls._session_factory.kw.get("bind")
            if bind is not None:
                await bind.dispose()
            cls._session_factory = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with PostgresSessionFactory.get_session() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
