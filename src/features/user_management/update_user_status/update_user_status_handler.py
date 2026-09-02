from src.features.user_management.shared.user import UserStatus
from itmentorsoft_persistence.repositories import UserRepository
from src.features.user_management.update_user_status.update_user_status_request import (
    UpdateUserStatusRequest,
)
from src.features.user_management.update_user_status.update_user_status_response import (
    UpdateUserStatusResponse,
)


class UpdateUserStatusHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(
        self, request: UpdateUserStatusRequest
    ) -> UpdateUserStatusResponse:

        is_valid_status = request.new_status in (member.value for member in UserStatus)
        if not is_valid_status:
            return UpdateUserStatusResponse(is_success=False, message="Invalid status")

        user = await self.user_repository.get_user_by_id(request.user_id)
        if not user:
            return UpdateUserStatusResponse(is_success=False, message="User not found")

        await self.user_repository.update_user_status(
            request.user_id, request.new_status
        )

        return UpdateUserStatusResponse(
            is_success=True, message="User status updated successfully"
        )
