import os
from dotenv import load_dotenv


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

load_dotenv()

DEFAULT_PASSWORD = os.getenv("DEFAULT_USER_PASSWORD", "")


class CreateUserFromAdminHandler:
    def __init__(self, user_manager_service: UserManagerService):
        self.user_manager_service = user_manager_service

    async def handle(
        self, request: CreateUserFromAdminRequest
    ) -> CreateUserFromAdminResponse:

        if not DEFAULT_PASSWORD:
            return CreateUserFromAdminResponse(
                is_success=False,
                message="Default password is not set in environment variables",
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
