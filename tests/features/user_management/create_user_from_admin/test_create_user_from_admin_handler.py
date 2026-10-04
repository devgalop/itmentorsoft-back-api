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
            is_success=True, message="Usuario creado exitosamente", user_id="user-123"
        )
    )

    with patch(
        "src.infrastructure.env_manager.env_manager.EnvironmentVariablesConstants.DEFAULT_USER_PASSWORD",
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
    assert response.message == "Usuario creado exitosamente"
    assert response.user_id == "user-123"
    user_manager_service.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_when_default_password_is_not_set_should_return_error():
    user_manager_service = AsyncMock()

    handler = CreateUserFromAdminHandler(user_manager_service)

    with patch(
        "src.infrastructure.env_manager.env_manager.EnvironmentVariablesConstants.DEFAULT_USER_PASSWORD",
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
    assert (
        response.message
        == "La contraseña por defecto no está configurada en las variables de entorno"
    )
    user_manager_service.create_user.assert_not_called()


@pytest.mark.asyncio
async def test_when_email_already_exists_should_return_error():
    user_manager_service = AsyncMock()
    user_manager_service.create_user = AsyncMock(
        return_value=CreateUserResponse(
            is_success=False, message="El email ya está en uso"
        )
    )

    with patch(
        "src.infrastructure.env_manager.env_manager.EnvironmentVariablesConstants.DEFAULT_USER_PASSWORD",
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
    assert response.message == "El email ya está en uso"
    assert response.user_id == ""


@pytest.mark.asyncio
async def test_when_username_already_exists_should_return_error():
    user_manager_service = AsyncMock()
    user_manager_service.create_user = AsyncMock(
        return_value=CreateUserResponse(
            is_success=False, message="El nombre de usuario ya está en uso"
        )
    )

    with patch(
        "src.infrastructure.env_manager.env_manager.EnvironmentVariablesConstants.DEFAULT_USER_PASSWORD",
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
    assert response.message == "El nombre de usuario ya está en uso"
    assert response.user_id == ""


@pytest.mark.asyncio
async def test_when_role_is_invalid_should_return_error():
    user_manager_service = AsyncMock()
    user_manager_service.create_user = AsyncMock(
        return_value=CreateUserResponse(
            is_success=False, message="Rol especificado inválido"
        )
    )
    with patch(
        "src.infrastructure.env_manager.env_manager.EnvironmentVariablesConstants.DEFAULT_USER_PASSWORD",
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
    assert response.message == "Rol especificado inválido"
    assert response.user_id == ""
