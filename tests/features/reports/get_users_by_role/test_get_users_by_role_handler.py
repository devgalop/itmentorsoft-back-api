from unittest.mock import AsyncMock
import pytest

from src.features.reports.get_users_by_role.get_users_by_role_handler import (
    GetUsersByRoleHandler,
)
from src.features.reports.get_users_by_role.get_users_by_role_request import (
    GetUsersByRoleRequest,
)
from src.features.reports.get_users_by_role.get_users_by_role_response import (
    GetUsersByRoleResponse,
)
from src.features.user_management.shared.user import UserResponse, UserRole, UserStatus
from src.features.user_management.shared.user_manager_service import (
    GetUsersByRoleResponse as ServiceGetUsersByRoleResponse,
    UserManagerService,
)


def make_service_response(
    users: list | None = None,
    is_success: bool = True,
    message: str = "Users retrieved successfully",
) -> ServiceGetUsersByRoleResponse:
    if users is None:
        users = [
            UserResponse(
                id="user-1",
                username="alice",
                email="alice@example.com",
                name="Alice Smith",
                status=UserStatus.ACTIVE,
                role=UserRole.ADMIN,
            ),
            UserResponse(
                id="user-2",
                username="bob",
                email="bob@example.com",
                name="Bob Johnson",
                status=UserStatus.ACTIVE,
                role=UserRole.ADMIN,
            ),
        ]
    return ServiceGetUsersByRoleResponse(
        is_success=is_success, message=message, users=users
    )


@pytest.mark.asyncio
async def test_when_users_exist_then_return_success_with_mapped_users():
    user_manager_service = AsyncMock(spec=UserManagerService)
    user_manager_service.get_users_by_role = AsyncMock(
        return_value=make_service_response()
    )

    handler = GetUsersByRoleHandler(user_manager_service)
    response = await handler.handle(GetUsersByRoleRequest(role="admin"))

    assert isinstance(response, GetUsersByRoleResponse)
    assert response.is_success is True
    assert response.message == "Users retrieved successfully"
    assert response.total_users == 2
    assert len(response.users) == 2
    assert response.users[0].user_id == "user-1"
    assert response.users[0].role == "admin"
    assert response.users[1].user_id == "user-2"
    assert response.users[1].role == "admin"


@pytest.mark.asyncio
async def test_when_service_returns_failure_then_return_failure_response():
    user_manager_service = AsyncMock(spec=UserManagerService)
    user_manager_service.get_users_by_role = AsyncMock(
        return_value=make_service_response(
            users=[], is_success=False, message="Invalid role specified"
        )
    )

    handler = GetUsersByRoleHandler(user_manager_service)
    response = await handler.handle(GetUsersByRoleRequest(role="unknown"))

    assert response.is_success is False
    assert response.message == "Invalid role specified"
    assert response.total_users == 0
    assert response.users == []


@pytest.mark.asyncio
async def test_when_no_users_found_then_return_empty_list():
    user_manager_service = AsyncMock(spec=UserManagerService)
    user_manager_service.get_users_by_role = AsyncMock(
        return_value=make_service_response(users=[])
    )

    handler = GetUsersByRoleHandler(user_manager_service)
    response = await handler.handle(GetUsersByRoleRequest(role="teacher"))

    assert response.is_success is True
    assert response.total_users == 0
    assert response.users == []


@pytest.mark.asyncio
async def test_handler_calls_service_with_correct_role():
    user_manager_service = AsyncMock(spec=UserManagerService)
    user_manager_service.get_users_by_role = AsyncMock(
        return_value=make_service_response()
    )

    handler = GetUsersByRoleHandler(user_manager_service)
    await handler.handle(GetUsersByRoleRequest(role="teacher"))

    user_manager_service.get_users_by_role.assert_called_once_with("teacher")


@pytest.mark.asyncio
async def test_handler_maps_multiple_roles_correctly():
    user_manager_service = AsyncMock(spec=UserManagerService)
    users = [
        UserResponse(
            id="user-a",
            username="charlie",
            email="charlie@example.com",
            name="Charlie Brown",
            status=UserStatus.ACTIVE,
            role=UserRole.TEACHER,
        ),
        UserResponse(
            id="user-b",
            username="diana",
            email="diana@example.com",
            name="Diana Prince",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        ),
    ]
    user_manager_service.get_users_by_role = AsyncMock(
        return_value=make_service_response(users=users)
    )

    handler = GetUsersByRoleHandler(user_manager_service)
    response = await handler.handle(GetUsersByRoleRequest(role="teacher"))

    assert response.total_users == 2
    assert response.users[0].user_id == "user-a"
    assert response.users[0].role == "teacher"
    assert response.users[1].user_id == "user-b"
    assert response.users[1].role == "student"
