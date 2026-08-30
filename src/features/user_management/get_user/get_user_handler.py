from src.features.user_management.get_user.get_user_request import GetUserRequest
from src.features.user_management.get_user.get_user_response import (
    GetUserResponse,
    UserResponse,
)
from src.features.user_management.shared.user_repository import UserRepository


class GetUserHandler:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, request: GetUserRequest) -> GetUserResponse:
        user = await self.user_repository.get_user_by_id(request.user_id)
        if not user:
            return GetUserResponse(is_success=False, message="User not found")

        return GetUserResponse(
            is_success=True,
            message="User found",
            user=UserResponse(
                user_id=user.id,
                username=user.username,
                email=user.email,
                name=user.name,
                role=user.role.value,
            ),
        )
