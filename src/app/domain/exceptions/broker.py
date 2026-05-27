from app.domain.exceptions.base import AppError


class BrokerPublishError(AppError):
    def __init__(self, message: str = "Failed to publish message to broker") -> None:
        super().__init__(message, code="broker_publish_error")
