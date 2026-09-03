from unittest.mock import AsyncMock
import pytest

from src.features.user_management.get_available_roles.get_available_roles_handler import (
    GetAvailableRolesHandler,
)
from itmentorsoft_persistence.dto import Role


@pytest.mark.asyncio
async def test_when_roles_exist_then_returns_success_with_role_name_list():
    role_repository = AsyncMock()
    role_repository.get_available_roles = AsyncMock(
        return_value=[
            Role(role_id="1", name="admin", description="Admin role"),
            Role(role_id="2", name="student", description="Student role"),
        ]
    )
    handler = GetAvailableRolesHandler(role_repository)

    response = await handler.handle()

    assert response.is_success is True
    assert response.roles == ["admin", "student"]


@pytest.mark.asyncio
async def test_when_repository_raises_exception_then_returns_failure_with_empty_roles():
    role_repository = AsyncMock()
    role_repository.get_available_roles = AsyncMock(side_effect=Exception("DB error"))
    handler = GetAvailableRolesHandler(role_repository)

    response = await handler.handle()

    assert response.is_success is False
    assert response.roles == []
