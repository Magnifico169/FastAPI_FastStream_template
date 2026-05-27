from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from app.domain.exceptions.broker import BrokerPublishError


@pytest.mark.asyncio
async def test_post_messages_returns_202(client: AsyncClient, mock_message_service: AsyncMock) -> None:
    response = await client.post("/messages", json={"text": "hello"})

    assert response.status_code == 202
    assert response.json() == {"status": "processing"}
    mock_message_service.enqueue.assert_awaited_once()


@pytest.mark.asyncio
async def test_post_messages_validation_422(client: AsyncClient) -> None:
    response = await client.post("/messages", json={"text": ""})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_messages_broker_error_503(client: AsyncClient, mock_message_service: AsyncMock) -> None:
    mock_message_service.enqueue.side_effect = BrokerPublishError("broker unavailable")

    response = await client.post("/messages", json={"text": "hello"})

    assert response.status_code == 503
    assert response.json()["code"] == "broker_publish_error"
