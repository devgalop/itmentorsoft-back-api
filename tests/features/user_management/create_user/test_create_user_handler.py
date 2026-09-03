from unittest.mock import Mock, AsyncMock
import pytest

from src.features.user_management.create_user.create_user_handler import (
    CreateUserHandler,
)
from src.features.user_management.create_user.create_user_request import (
    CreateUserRequest,
)
from itmentorsoft_persistence.dto import Role


@pytest.mark.asyncio
async def test_when_user_is_valid_should_create_user():

    user_repository = AsyncMock()
    password_hasher = Mock()

    user_repository.get_user_by_email = AsyncMock(return_value=None)
    user_repository.get_user_by_username = AsyncMock(return_value=None)
    password_hasher.hash_password = Mock(return_value="hashed_password")
    role_repository = AsyncMock()
    role_repository.get_role_by_name = AsyncMock(
        return_value=Role(
            role_id="1", name="student", description="Default student role"
        )
    )

    handler = CreateUserHandler(user_repository, password_hasher, role_repository)
    await handler.handle(
        CreateUserRequest(
            email="test@example.com",
            password="StrongPassword123!",
            username="testuser",
            name="Test User",
        )
    )

    user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    user_repository.get_user_by_username.assert_called_once_with("testuser")
    password_hasher.hash_password.assert_called_once_with("StrongPassword123!")
    role_repository.get_role_by_name.assert_called_once_with("student")
    user_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_when_email_already_exists_should_respond_with_error():

    user_repository = AsyncMock()
    password_hasher = Mock()

    user_repository.get_user_by_email = AsyncMock(
        return_value={"email": "test@example.com"}
    )
    role_repository = AsyncMock()
    role_repository.get_role_by_name = AsyncMock()
    handler = CreateUserHandler(user_repository, password_hasher, role_repository)
    response = await handler.handle(
        CreateUserRequest(
            email="test@example.com",
            password="StrongPassword123!",
            username="testuser",
            name="Test User",
        )
    )
    assert not response.is_success
    assert response.message == "Email already in use"
    user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    user_repository.get_user_by_username.assert_not_called()
    password_hasher.hash_password.assert_not_called()
    role_repository.get_role_by_name.assert_not_called()
    user_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_when_username_already_exists_should_respond_with_error():

    user_repository = AsyncMock()
    password_hasher = Mock()

    user_repository.get_user_by_email = AsyncMock(return_value=None)
    user_repository.get_user_by_username = AsyncMock(
        return_value={"username": "testuser"}
    )
    role_repository = AsyncMock()
    role_repository.get_role_by_name = AsyncMock()

    handler = CreateUserHandler(user_repository, password_hasher, role_repository)
    response = await handler.handle(
        CreateUserRequest(
            email="test@example.com",
            password="StrongPassword123!",
            username="testuser",
            name="Test User",
        )
    )
    assert not response.is_success
    assert response.message == "Username already in use"
    user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    user_repository.get_user_by_username.assert_called_once_with("testuser")
    password_hasher.hash_password.assert_not_called()
    role_repository.get_role_by_name.assert_not_called()
    user_repository.save.assert_not_called()
