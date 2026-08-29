from unittest.mock import AsyncMock
import pytest

from src.features.user_management.get_user.get_user_handler import GetUserHandler
from src.features.user_management.get_user.get_user_request import GetUserRequest
from src.features.user_management.get_user.get_user_response import GetUserResponse
from src.features.user_management.shared.user import UserResponse, UserRole, UserStatus


@pytest.mark.asyncio
async def test_when_user_exists_should_return_user():

    user_repository = AsyncMock()
    user_response = UserResponse(
        id="123",
        username="testuser",
        email="testuser@example.com",
        name="Test User",
        status=UserStatus("active"),
        role=UserRole("student"),
    )
    user_repository.get_user_by_id = AsyncMock(return_value=user_response)
    handler = GetUserHandler(user_repository)
    response = await handler.handle(GetUserRequest(user_id="123"))
    assert isinstance(response, GetUserResponse)
    assert response.is_success
    assert response.message == "User found"
    user_repository.get_user_by_id.assert_called_once_with("123")


@pytest.mark.asyncio
async def test_when_user_does_not_exist_should_return_not_found():

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=None)
    handler = GetUserHandler(user_repository)
    response = await handler.handle(GetUserRequest(user_id="123"))
    assert isinstance(response, GetUserResponse)
    assert not response.is_success
    assert response.message == "User not found"
    user_repository.get_user_by_id.assert_called_once_with("123")
