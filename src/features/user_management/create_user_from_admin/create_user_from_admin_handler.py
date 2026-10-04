from src.features.user_management.create_user_from_admin.create_user_from_admin_request import (
    CreateUserFromAdminRequest,
)
from src.features.user_management.create_user_from_admin.create_user_from_admin_response import (
    CreateUserFromAdminResponse,
)
from src.features.user_management.shared.user_manager_service import (
    CreateUserRequest,
    UserManagerService,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants
from src.i18n import t


class CreateUserFromAdminHandler:
    def __init__(self, user_manager_service: UserManagerService):
        self.user_manager_service = user_manager_service

    async def handle(
        self, request: CreateUserFromAdminRequest
    ) -> CreateUserFromAdminResponse:

        DEFAULT_PASSWORD = EnvironmentVariablesConstants.DEFAULT_USER_PASSWORD

        if not DEFAULT_PASSWORD:
            return CreateUserFromAdminResponse(
                is_success=False,
                message=t("user.admin.default_password_not_set"),
            )

        response = await self.user_manager_service.create_user(
            request=CreateUserRequest(
                email=request.email,
                name=request.name,
                username=request.username,
                password=DEFAULT_PASSWORD,
                role=request.role,
            )
        )

        return CreateUserFromAdminResponse(
            is_success=response.is_success,
            message=response.message,
            user_id=response.user_id,
        )
