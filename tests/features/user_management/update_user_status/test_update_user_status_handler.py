from unittest.mock import AsyncMock

import pytest

from itmentorsoft_persistence.dto import (
    CompleteUserResponse,
    UserRole,
    UserStatus,
)
from src.features.user_management.update_user_status.update_user_status_handler import (
    UpdateUserStatusHandler,
)
from src.features.user_management.update_user_status.update_user_status_request import (
    UpdateUserStatusRequest,
)


@pytest.mark.asyncio
async def test_when_status_is_valid_and_user_exists_should_update_status():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(
        return_value=CompleteUserResponse(
            id="user_id",
            username="testuser",
            email="test@example.com",
            password_hashed="hashed_password",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )
    user_repository.update_user_status = AsyncMock()

    handler = UpdateUserStatusHandler(user_repository)
    response = await handler.handle(
        UpdateUserStatusRequest(user_id="user_id", new_status="inactive")
    )

    assert response.is_success
    assert response.message == "User status updated successfully"
    user_repository.get_user_by_id.assert_called_once_with("user_id")
    user_repository.update_user_status.assert_called_once_with("user_id", "inactive")


@pytest.mark.asyncio
async def test_when_status_is_invalid_should_return_error():
    user_repository = AsyncMock()

    handler = UpdateUserStatusHandler(user_repository)
    response = await handler.handle(
        UpdateUserStatusRequest(user_id="user_id", new_status="invalid_status")
    )

    assert not response.is_success
    assert response.message == "Invalid status"
    user_repository.get_user_by_id.assert_not_called()
    user_repository.update_user_status.assert_not_called()


@pytest.mark.asyncio
async def test_when_user_does_not_exist_should_return_error():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=None)

    handler = UpdateUserStatusHandler(user_repository)
    response = await handler.handle(
        UpdateUserStatusRequest(user_id="nonexistent_id", new_status="active")
    )

    assert not response.is_success
    assert response.message == "User not found"
    user_repository.get_user_by_id.assert_called_once_with("nonexistent_id")
    user_repository.update_user_status.assert_not_called()
