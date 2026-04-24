from enum import StrEnum


class MessageStatus(StrEnum):
    PROCESSING = "processing"
    ERROR = "error"
    OK = "ok"
