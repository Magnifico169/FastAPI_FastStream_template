from collections.abc import AsyncIterator
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app
from app.services.dependencies import get_message_service


@pytest.fixture
async def mock_message_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
async def client(mock_message_service: AsyncMock) -> AsyncIterator[AsyncClient]:
    app = create_app()
    app.dependency_overrides[get_message_service] = lambda: mock_message_service

    with (
        patch("app.main.PostgresSessionFactory.initialize", new=AsyncMock()),
        patch("app.main.PostgresSessionFactory.close", new=AsyncMock()),
        patch("app.main.rabbit_broker.start", new=AsyncMock()),
        patch("app.main.rabbit_broker.stop", new=AsyncMock()),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as async_client:
            yield async_client

    app.dependency_overrides.clear()
