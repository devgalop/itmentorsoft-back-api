from unittest.mock import AsyncMock
import pytest

from src.features.user_management.get_connected_users.get_connected_users_handler import (
    GetConnectedUsersHandler,
)
from itmentorsoft_persistence import TotalActiveUsers


@pytest.mark.asyncio
async def test_when_there_are_active_users_should_return_success_response():
    repository = AsyncMock()
    repository.get_users_with_active_tokens = AsyncMock(
        return_value=TotalActiveUsers(total_users=5)
    )

    handler = GetConnectedUsersHandler(repository)
    response = await handler.handle()

    assert response.is_success is True
    assert response.message == "Users connected have been found successfully"
    assert response.total_users == 5
    repository.get_users_with_active_tokens.assert_called_once()


@pytest.mark.asyncio
async def test_when_there_are_no_active_users_should_return_failure_response():
    repository = AsyncMock()
    repository.get_users_with_active_tokens = AsyncMock(
        return_value=TotalActiveUsers(total_users=0)
    )

    handler = GetConnectedUsersHandler(repository)
    response = await handler.handle()

    assert response.is_success is False
    assert response.message == "Cannot obtain any connected users"
    assert response.total_users == 0
    repository.get_users_with_active_tokens.assert_called_once()


@pytest.mark.asyncio
async def test_when_there_is_exactly_one_active_user_should_return_success_response():
    repository = AsyncMock()
    repository.get_users_with_active_tokens = AsyncMock(
        return_value=TotalActiveUsers(total_users=1)
    )

    handler = GetConnectedUsersHandler(repository)
    response = await handler.handle()

    assert response.is_success is True
    assert response.total_users == 1
    repository.get_users_with_active_tokens.assert_called_once()
