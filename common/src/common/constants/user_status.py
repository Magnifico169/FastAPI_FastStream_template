from enum import StrEnum


class UserStatus(StrEnum):
    """User status."""

    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
