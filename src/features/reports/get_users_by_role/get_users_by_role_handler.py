from src.features.reports.get_users_by_role.get_users_by_role_request import (
    GetUsersByRoleRequest,
)
from src.features.reports.get_users_by_role.get_users_by_role_response import (
    GetUsersByRoleResponse,
    UserByRole,
)
from src.features.user_management.shared.user_manager_service import UserManagerService


class GetUsersByRoleHandler:
    def __init__(self, user_manager_service: UserManagerService):
        self.user_manager_service = user_manager_service

    async def handle(self, request: GetUsersByRoleRequest) -> GetUsersByRoleResponse:

        result = await self.user_manager_service.get_users_by_role(request.role)
        if not result.is_success:
            return GetUsersByRoleResponse(
                is_success=False, message=result.message, total_users=0, users=[]
            )

        users = [
            UserByRole(user_id=user.id, role=user.role.value) for user in result.users
        ]
        return GetUsersByRoleResponse(
            is_success=True,
            message="Users retrieved successfully",
            total_users=len(users),
            users=users,
        )
