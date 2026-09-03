from itmentorsoft_persistence.repositories import UserRepository
from src.features.user_management.update_user_profile.update_user_profile_request import (
    UpdateUserProfileRequest,
)
from src.features.user_management.update_user_profile.update_user_profile_response import (
    UpdateUserProfileResponse,
)


class UpdateUserProfileHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(
        self, request: UpdateUserProfileRequest
    ) -> UpdateUserProfileResponse:

        existing_user = await self.user_repository.get_user_by_id(request.user_id)
        if not existing_user:
            return UpdateUserProfileResponse(is_success=False, message="User not found")

        existing_user_with_username = await self.user_repository.get_user_by_username(
            request.username
        )
        if (
            existing_user_with_username
            and existing_user_with_username.id != request.user_id
        ):
            return UpdateUserProfileResponse(
                is_success=False, message="Username is not available"
            )

        await self.user_repository.update_username(
            request.user_id, request.username, request.name
        )
        return UpdateUserProfileResponse(
            is_success=True, message="Username and name updated successfully"
        )
