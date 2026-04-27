from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from typing import Annotated, ClassVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from common.settings import get_postgres_settings
from common.exceptions import SessionFactoryAlreadyInitializedError


class PostgresSessionFactory:
    """
    Factory class for creating PostgreSQL database sessions.

    Provides class methods for session creation without instantiation.
    Session factory is stored as a class variable (Singleton pattern).
    """

    _session_factory: ClassVar[async_sessionmaker[AsyncSession] | None] = None

    @classmethod
    async def initialize(cls) -> None:
        """
        Initialize the global session factory with given settings.

        :raises RuntimeError: if already initialized
        """
        postgres_settings = get_postgres_settings()
        if cls._session_factory is not None:
            raise SessionFactoryAlreadyInitializedError

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
        """
        Create and return a database session.

        Session lifecycle must be managed by the caller.
        Use as context manager for automatic cleanup.

        :returns: AsyncSession instance
        :raises RuntimeError: if factory not initialized

        Example::

            async with PostgresSessionFactory.get_session() as session:
                result = await session.execute(query)
        """
        if cls._session_factory is None:
            raise SessionFactoryAlreadyInitializedError

        session = cls._session_factory()
        try:
            yield session
        finally:
            await session.close()

    @classmethod
    async def close(cls) -> None:
        """
        Close all database connections and clean up resources.

        Should be called during application shutdown.
        """
        if cls._session_factory is not None:
            engine = cls._session_factory.kw["bind"]
            await engine.dispose()
            cls._session_factory = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with PostgresSessionFactory.get_session() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
