from unittest.mock import AsyncMock

import pytest

from src.features.user_management.update_user_profile.update_user_profile_handler import (
    UpdateUserProfileHandler,
)
from src.features.user_management.update_user_profile.update_user_profile_request import (
    UpdateUserProfileRequest,
)
from src.features.user_management.shared.user import (
    CompleteUserResponse,
    UserRole,
    UserStatus,
)


@pytest.mark.asyncio
async def test_when_user_does_not_exist_should_return_failure():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=None)

    handler = UpdateUserProfileHandler(user_repository)
    response = await handler.handle(
        UpdateUserProfileRequest(
            user_id="non_existent_id", username="new_username", name="New Name"
        )
    )

    assert not response.is_success
    assert response.message == "User not found"
    user_repository.get_user_by_id.assert_called_once_with("non_existent_id")
    user_repository.get_user_by_username.assert_not_called()
    user_repository.update_username.assert_not_called()


@pytest.mark.asyncio
async def test_when_username_is_taken_by_another_user_should_return_failure():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(
        return_value=CompleteUserResponse(
            id="user_id",
            username="old_username",
            email="test@example.com",
            password_hashed="hashed",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )
    user_repository.get_user_by_username = AsyncMock(
        return_value=CompleteUserResponse(
            id="other_user_id",
            username="taken_username",
            email="other@example.com",
            password_hashed="hashed",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )

    handler = UpdateUserProfileHandler(user_repository)
    response = await handler.handle(
        UpdateUserProfileRequest(
            user_id="user_id", username="taken_username", name="New Name"
        )
    )

    assert not response.is_success
    assert response.message == "Username is not available"
    user_repository.get_user_by_id.assert_called_once_with("user_id")
    user_repository.get_user_by_username.assert_called_once_with("taken_username")
    user_repository.update_username.assert_not_called()


@pytest.mark.asyncio
async def test_when_username_belongs_to_same_user_should_update_successfully():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(
        return_value=CompleteUserResponse(
            id="user_id",
            username="old_username",
            email="test@example.com",
            password_hashed="hashed",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )
    user_repository.get_user_by_username = AsyncMock(
        return_value=CompleteUserResponse(
            id="user_id",
            username="old_username",
            email="test@example.com",
            password_hashed="hashed",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )
    user_repository.update_username = AsyncMock()

    handler = UpdateUserProfileHandler(user_repository)
    response = await handler.handle(
        UpdateUserProfileRequest(
            user_id="user_id", username="old_username", name="New Name"
        )
    )

    assert response.is_success
    assert response.message == "Username and name updated successfully"
    user_repository.update_username.assert_called_once_with(
        "user_id", "old_username", "New Name"
    )


@pytest.mark.asyncio
async def test_when_user_exists_and_username_is_available_should_update_successfully():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(
        return_value=CompleteUserResponse(
            id="user_id",
            username="old_username",
            email="test@example.com",
            password_hashed="hashed",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )
    user_repository.get_user_by_username = AsyncMock(return_value=None)
    user_repository.update_username = AsyncMock()

    handler = UpdateUserProfileHandler(user_repository)
    response = await handler.handle(
        UpdateUserProfileRequest(
            user_id="user_id", username="new_username", name="New Name"
        )
    )

    assert response.is_success
    assert response.message == "Username and name updated successfully"
    user_repository.get_user_by_id.assert_called_once_with("user_id")
    user_repository.get_user_by_username.assert_called_once_with("new_username")
    user_repository.update_username.assert_called_once_with(
        "user_id", "new_username", "New Name"
    )
