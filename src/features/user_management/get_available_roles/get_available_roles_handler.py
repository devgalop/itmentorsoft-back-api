from src.features.user_management.get_available_roles.get_available_roles_response import (
    GetAvailableRolesResponse,
    RoleDetail,
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
                is_success=True,
                roles=[
                    RoleDetail(
                        id=role.role_id,
                        name=role.name,
                        homologate_name=self._get_homologate_role(role.name),
                    )
                    for role in roles
                ],
            )
        except Exception:
            return GetAvailableRolesResponse(is_success=False, roles=[])

    def _get_homologate_role(self, name: str) -> str:
        """Get the homologate role name based on the provided name.

        Args:
            name (str): The name of the role.

        Returns:
            str: The homologate role name.
        """
        homologate_roles = {
            "admin": "Administrador",
            "teacher": "Profesor",
            "student": "Estudiante",
            "user": "Invitado",
        }
        return homologate_roles.get(name.lower(), name)
