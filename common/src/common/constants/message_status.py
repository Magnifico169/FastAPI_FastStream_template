from enum import StrEnum


class MessageStatus(StrEnum):
    """Message status."""

    PROCESSING = "PROCESSING"
    ERROR = "ERROR"
    OK = "OK"
