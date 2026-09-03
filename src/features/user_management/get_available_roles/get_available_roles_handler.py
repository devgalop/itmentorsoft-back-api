from src.features.user_management.get_available_roles.get_available_roles_response import (
    GetAvailableRolesResponse,
)
from itmentorsoft_persistence.repositories import RoleRepository


class GetAvailableRolesHandler:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    async def handle(self) -> GetAvailableRolesResponse:
        """Handle the request to get available roles.

        Returns:
            GetAvailableRolesResponse: A response object containing the list of available roles.
        """
        try:
            roles = await self.role_repository.get_available_roles()
            return GetAvailableRolesResponse(
                is_success=True, roles=[role.name for role in roles]
            )
        except Exception:
            return GetAvailableRolesResponse(is_success=False, roles=[])
