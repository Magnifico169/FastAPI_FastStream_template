from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.domain.dto.message_create import MessageCreateDTO
from app.domain.enums.message_status import MessageStatus
from app.domain.exceptions.broker import BrokerPublishError
from app.domain.exceptions.persistence import MessagePersistenceError
from app.domain.models.message import Message
from app.services.message_service import MessageService


@pytest.mark.asyncio
async def test_enqueue_publishes_message() -> None:
    repository = AsyncMock()
    service = MessageService(repository)

    with patch("app.services.message_service.rabbit_broker.publish", new=AsyncMock()) as mock_publish:
        await service.enqueue(MessageCreateDTO(text="hello"))

    mock_publish.assert_awaited_once()
    published_message = mock_publish.await_args.args[0]
    assert published_message.text == "hello"
    assert published_message.status == MessageStatus.PROCESSING


@pytest.mark.asyncio
async def test_enqueue_raises_broker_error() -> None:
    repository = AsyncMock()
    service = MessageService(repository)

    with (
        patch(
            "app.services.message_service.rabbit_broker.publish",
            new=AsyncMock(side_effect=ConnectionError("broker down")),
        ),
        pytest.raises(BrokerPublishError),
    ):
        await service.enqueue(MessageCreateDTO(text="hello"))


@pytest.mark.asyncio
async def test_process_saves_message() -> None:
    repository = AsyncMock()
    saved = Message(id=uuid4(), text="hello", status=MessageStatus.PROCESSED)
    repository.create.return_value = saved
    service = MessageService(repository)

    result = await service.process(Message(text="hello", status=MessageStatus.PROCESSING))

    repository.create.assert_awaited_once()
    create_arg = repository.create.await_args.args[0]
    assert create_arg.status == MessageStatus.PROCESSED
    assert result == saved


@pytest.mark.asyncio
async def test_process_raises_persistence_error() -> None:
    repository = AsyncMock()
    repository.create.side_effect = MessagePersistenceError("db error")
    service = MessageService(repository)

    with pytest.raises(MessagePersistenceError):
        await service.process(Message(text="hello", status=MessageStatus.PROCESSING))
