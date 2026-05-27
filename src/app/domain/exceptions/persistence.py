from app.domain.exceptions.base import AppError


class MessagePersistenceError(AppError):
    def __init__(self, message: str = "Failed to persist message") -> None:
        super().__init__(message, code="message_persistence_error")
