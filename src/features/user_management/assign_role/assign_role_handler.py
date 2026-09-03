from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)
from src.features.user_management.assign_role.assign_role_response import (
    AssignRoleResponse,
)
from itmentorsoft_persistence.dto import (
    AssignRoleToUserCommand as AssignRoleToUserCommandDTO,
)
from itmentorsoft_persistence.repositories import RoleRepository, UserRepository


class AssignRoleHandler:
    def __init__(
        self, user_repository: UserRepository, role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def handle(self, request: AssignRoleRequest) -> AssignRoleResponse:
        """Handle the role assignment request.

        Args:
            request (AssignRoleRequest): The request object containing user ID and role information.

        Returns:
            AssignRoleResponse: The response object containing the result of the role assignment.
        """
        try:
            available_roles = await self.role_repository.get_available_roles()
            if request.role not in [role.name for role in available_roles]:
                return AssignRoleResponse(
                    is_success=False, message="Invalid role specified."
                )
            role_selected = available_roles[
                [role.name for role in available_roles].index(request.role)
            ]
            assign_role_command = AssignRoleToUserCommandDTO(
                user_id=request.user_id, role_id=role_selected.role_id
            )
            await self.user_repository.assign_role_to_user(assign_role_command)
            return AssignRoleResponse(
                is_success=True, message="Role assigned successfully."
            )
        except Exception as e:
            return AssignRoleResponse(is_success=False, message=str(e))
