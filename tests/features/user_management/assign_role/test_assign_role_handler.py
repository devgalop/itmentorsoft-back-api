from unittest.mock import AsyncMock
import pytest

from src.features.user_management.assign_role.assign_role_handler import (
    AssignRoleHandler,
)
from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)
from itmentorsoft_persistence.dto import Role


@pytest.mark.asyncio
async def test_when_role_is_valid_then_should_assign_role_successfully():
    user_repository = AsyncMock()
    user_repository.get_available_roles = AsyncMock(
        return_value=["admin", "editor", "viewer"]
    )
    role_repository = AsyncMock()
    role_repository.get_available_roles = AsyncMock(
        return_value=[
            Role(role_id="1", name="admin", description="Admin role"),
            Role(role_id="2", name="editor", description="Editor role"),
        ]
    )
    handler = AssignRoleHandler(user_repository, role_repository)

    request = AssignRoleRequest(user_id="user123", role="editor")
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Role assigned successfully."
    role_repository.get_available_roles.assert_called_once()
    user_repository.assign_role_to_user.assert_called_once()


@pytest.mark.asyncio
async def test_when_role_is_invalid_then_should_respond_with_error():
    user_repository = AsyncMock()
    user_repository.get_available_roles = AsyncMock(
        return_value=["admin", "editor", "viewer"]
    )
    role_repository = AsyncMock()
    role_repository.get_available_roles = AsyncMock(
        return_value=[
            Role(role_id="1", name="admin", description="Admin role"),
            Role(role_id="2", name="editor", description="Editor role"),
        ]
    )
    handler = AssignRoleHandler(user_repository, role_repository)

    request = AssignRoleRequest(user_id="user123", role="invalid_role")
    response = await handler.handle(request)

    assert not response.is_success
    assert response.message == "Invalid role specified."
    role_repository.get_available_roles.assert_called_once()
    user_repository.assign_role_to_user.assert_not_called()


@pytest.mark.asyncio
async def test_when_repository_raises_exception_then_should_return_failure():
    role_repository = AsyncMock()
    role_repository.get_available_roles = AsyncMock(
        side_effect=Exception("Database connection failed")
    )
    user_repository = AsyncMock()
    handler = AssignRoleHandler(user_repository, role_repository)

    request = AssignRoleRequest(user_id="user123", role="admin")
    response = await handler.handle(request)

    assert not response.is_success
    assert "Database connection failed" in response.message
    user_repository.assign_role_to_user.assert_not_called()
