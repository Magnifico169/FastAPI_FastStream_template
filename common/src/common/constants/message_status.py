from enum import StrEnum


class MessageStatus(StrEnum):
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"
    OK = "OK"
