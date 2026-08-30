from src.features.user_management.get_connected_users.get_connected_users_response import (
    GetConnectedUsersResponse,
)
from src.features.user_management.shared.refresh_token_repository import (
    RefreshTokenRepository,
)


class GetConnectedUsersHandler:
    def __init__(self, repository: RefreshTokenRepository):
        self.repository = repository

    async def handle(self) -> GetConnectedUsersResponse:
        response = await self.repository.get_users_with_active_tokens()
        if response.total_users <= 0:
            return GetConnectedUsersResponse(
                is_success=False,
                message="Cannot obtain any connected users",
                total_users=0,
            )
        return GetConnectedUsersResponse(
            is_success=True,
            message="Users connected have been found successfully",
            total_users=response.total_users,
        )
