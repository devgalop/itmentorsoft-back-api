from src.features.user_management.get_connected_users.get_connected_users_response import (
    GetConnectedUsersResponse,
)
from itmentorsoft_persistence.repositories import (
    RefreshTokenRepository,
)
from src.i18n import t


class GetConnectedUsersHandler:
    def __init__(self, repository: RefreshTokenRepository):
        self.repository = repository

    async def handle(self) -> GetConnectedUsersResponse:
        response = await self.repository.get_users_with_active_tokens()
        if response.total_users <= 0:
            return GetConnectedUsersResponse(
                is_success=False,
                message=t("user.connected.none"),
                total_users=0,
            )
        return GetConnectedUsersResponse(
            is_success=True,
            message=t("user.connected.found"),
            total_users=response.total_users,
        )
