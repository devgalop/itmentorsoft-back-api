from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.token_generator import TokenGenerator
from itmentorsoft_persistence.dto import (
    RecoveryTokenInfo,
)
from itmentorsoft_persistence.repositories import (
    UserRecoveryTokenRepository,
)
from src.features.shared.template_loader import TemplateLoader
from src.features.user_management.recovery_password.recovery_password_request import (
    RecoveryPasswordRequest,
)
from src.features.user_management.recovery_password.recovery_password_response import (
    RecoveryPasswordResponse,
)
from itmentorsoft_persistence.repositories import UserRepository
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants
from src.i18n import t
from src.infrastructure.notification.notification_message import (
    RecoverPasswordNotifyRequest,
)
from src.infrastructure.notification.notificator_service import NotificatorService

EMAIL_RECOVERY_SUBJECT = t("user.recovery.subject")
RECOVERY_URL_BASE = EnvironmentVariablesConstants.RECOVERY_URL_BASE


class RecoveryPasswordHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        user_recovery_token_repository: UserRecoveryTokenRepository,
        notification_service: NotificatorService,
        token_generator: TokenGenerator,
        password_hasher: PasswordHasher,
        template_loader: TemplateLoader,
    ):
        self.user_repository = user_repository
        self.user_recovery_token_repository = user_recovery_token_repository
        self.notification_service = notification_service
        self.token_generator = token_generator
        self.password_hasher = password_hasher
        self.template_loader = template_loader

    async def handle(
        self, request: RecoveryPasswordRequest
    ) -> RecoveryPasswordResponse:

        if not RECOVERY_URL_BASE:
            return RecoveryPasswordResponse(message=t("user.recovery.url_not_set"))
        response_message = t("user.recovery.email_sent")
        user = await self.user_repository.get_user_response_by_email(request.email)
        if not user:
            return RecoveryPasswordResponse(message=response_message)

        await self.user_recovery_token_repository.revoke_tokens_by_user_id(user.id)
        token = self.token_generator.generate_random_token()
        hashed_token = self.password_hasher.hash_password(token.token)
        recovery_token_info = RecoveryTokenInfo(
            user_id=user.id,
            token=hashed_token,
            expiration_time=token.expiration_time,
            status="active",
        )

        await self.user_recovery_token_repository.save_token(recovery_token_info)

        _ = await self.notification_service.send_recovery_notification(
            RecoverPasswordNotifyRequest(
                recipient=user.email,
                id_trx=recovery_token_info.id_trx,
                url_token=token.token,
                url_base=RECOVERY_URL_BASE,
                user=user.username,
            )
        )

        return RecoveryPasswordResponse(message=response_message)
