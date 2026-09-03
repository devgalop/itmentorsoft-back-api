import time

from src.features.user_management.change_password.change_password_request import (
    ChangePasswordRequestWithToken,
)
from src.features.user_management.change_password.change_password_response import (
    ChangePasswordResponse,
)
from src.features.user_management.shared.password_hasher import PasswordHasher
from itmentorsoft_persistence.repositories import (
    UserRecoveryTokenRepository,
    UserRepository,
)


class ChangePasswordHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        user_recovery_token_repository: UserRecoveryTokenRepository,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.user_recovery_token_repository = user_recovery_token_repository
        self.password_hasher = password_hasher

    async def handle(
        self, request: ChangePasswordRequestWithToken
    ) -> ChangePasswordResponse:
        user_recover_info = (
            await self.user_recovery_token_repository.get_user_id_by_transaction_id(
                request.id_trx
            )
        )
        if (
            not user_recover_info
            or user_recover_info.expiration_time < time.time()
            or not self.password_hasher.verify_password(
                request.token, user_recover_info.token_hashed
            )
        ):
            return ChangePasswordResponse(
                is_success=False, message="Invalid or expired token"
            )

        user = await self.user_repository.get_user_by_id(user_recover_info.user_id)
        if not user:
            return ChangePasswordResponse(is_success=False, message="User not found")

        await self.user_recovery_token_repository.revoke_tokens_by_user_id(
            user_recover_info.user_id
        )
        hashed_password = self.password_hasher.hash_password(request.new_password)
        await self.user_repository.change_password(
            user_recover_info.user_id, hashed_password
        )

        return ChangePasswordResponse(
            is_success=True, message="Password changed successfully"
        )
