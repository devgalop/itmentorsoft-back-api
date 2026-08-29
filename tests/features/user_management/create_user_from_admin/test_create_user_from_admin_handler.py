from unittest.mock import AsyncMock, patch
import pytest

from src.features.user_management.create_user_from_admin.create_user_from_admin_handler import (
    CreateUserFromAdminHandler,
)
from src.features.user_management.create_user_from_admin.create_user_from_admin_request import (
    CreateUserFromAdminRequest,
)
from src.features.user_management.shared.user_manager_service import CreateUserResponse


@pytest.mark.asyncio
async def test_when_user_is_valid_should_create_user():
    user_manager_service = AsyncMock()
    user_manager_service.create_user = AsyncMock(
        return_value=CreateUserResponse(
            is_success=True, message="User created successfully", user_id="user-123"
        )
    )

    with patch(
        "src.features.user_management.create_user_from_admin.create_user_from_admin_handler.DEFAULT_PASSWORD",
        "default_password",
    ):
        handler = CreateUserFromAdminHandler(user_manager_service)
        response = await handler.handle(
            CreateUserFromAdminRequest(
                email="test@example.com",
                username="testuser",
                role="student",
                name="Test User",
            )
        )

    assert response.is_success
    assert response.message == "User created successfully"
    assert response.user_id == "user-123"
    user_manager_service.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_when_default_password_is_not_set_should_return_error():
    user_manager_service = AsyncMock()

    handler = CreateUserFromAdminHandler(user_manager_service)

    with patch(
        "src.features.user_management.create_user_from_admin.create_user_from_admin_handler.DEFAULT_PASSWORD",
        "",
    ):
        response = await handler.handle(
            CreateUserFromAdminRequest(
                email="test@example.com",
                username="testuser",
                role="student",
                name="Test User",
            )
        )

    assert not response.is_success
    assert response.message == "Default password is not set in environment variables"
    user_manager_service.create_user.assert_not_called()


@pytest.mark.asyncio
async def test_when_email_already_exists_should_return_error():
    user_manager_service = AsyncMock()
    user_manager_service.create_user = AsyncMock(
        return_value=CreateUserResponse(
            is_success=False, message="Email already in use"
        )
    )

    with patch(
        "src.features.user_management.create_user_from_admin.create_user_from_admin_handler.DEFAULT_PASSWORD",
        "default_password",
    ):

        handler = CreateUserFromAdminHandler(user_manager_service)
        response = await handler.handle(
            CreateUserFromAdminRequest(
                email="test@example.com",
                username="testuser",
                role="student",
                name="Test User",
            )
        )

    assert not response.is_success
    assert response.message == "Email already in use"
    assert response.user_id == ""


@pytest.mark.asyncio
async def test_when_username_already_exists_should_return_error():
    user_manager_service = AsyncMock()
    user_manager_service.create_user = AsyncMock(
        return_value=CreateUserResponse(
            is_success=False, message="Username already in use"
        )
    )

    with patch(
        "src.features.user_management.create_user_from_admin.create_user_from_admin_handler.DEFAULT_PASSWORD",
        "default_password",
    ):
        handler = CreateUserFromAdminHandler(user_manager_service)
        response = await handler.handle(
            CreateUserFromAdminRequest(
                email="test@example.com",
                username="testuser",
                role="student",
                name="Test User",
            )
        )

    assert not response.is_success
    assert response.message == "Username already in use"
    assert response.user_id == ""


@pytest.mark.asyncio
async def test_when_role_is_invalid_should_return_error():
    user_manager_service = AsyncMock()
    user_manager_service.create_user = AsyncMock(
        return_value=CreateUserResponse(
            is_success=False, message="Invalid role specified"
        )
    )
    with patch(
        "src.features.user_management.create_user_from_admin.create_user_from_admin_handler.DEFAULT_PASSWORD",
        "default_password",
    ):

        handler = CreateUserFromAdminHandler(user_manager_service)
        response = await handler.handle(
            CreateUserFromAdminRequest(
                email="test@example.com",
                username="testuser",
                role="invalid_role",
                name="Test User",
            )
        )

    assert not response.is_success
    assert response.message == "Invalid role specified"
    assert response.user_id == ""
