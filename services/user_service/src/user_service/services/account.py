import logging
from typing import Annotated

from fastapi import Depends

from common.domain import User
from user_service.repositories import (
    UsersRepository,
    UsersRepositoryDependence,
)

logger = logging.getLogger(__name__)


class AccountService:
    """Account service."""

    def __init__(self, user_repository: UsersRepository) -> None:
        """
        Init Account Service.

        :param user_repository: UsersRepositoryDependence
        :return: None
        """
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        """
        Create new user.

        :param user:
        :return:
        """
        return await self.user_repository.create(user)


def get_account_service(
    user_repository: UsersRepositoryDependence,
) -> AccountService:
    """Get Account Service."""
    return AccountService(user_repository)


AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]
