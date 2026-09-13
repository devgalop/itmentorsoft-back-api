from src.features.shared.notification_service import (
    NotificationService,
)
from src.features.shared.template_loader import TemplateLoader
from src.features.user_management.login.login_request import LoginRequest
from src.features.user_management.login.login_response import LoginResponse
from src.features.user_management.shared.password_hasher import PasswordHasher
from itmentorsoft_persistence.repositories import UserRepository
from src.features.user_management.shared.user_manager_service import (
    UserManagerService,
    UserOTPNotificationRequest,
)


class LoginHandler:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        notification_service: NotificationService,
        template_loader: TemplateLoader,
        user_manager_service: UserManagerService,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.user_manager_service = user_manager_service
        self.notification_service = notification_service
        self.template_loader = template_loader

    async def handle(self, request: LoginRequest) -> LoginResponse:
        """ "Handle the login request.

        Args:
            request (LoginRequest): The login request containing the user's email and password.
        Returns:
            LoginResponse: The response indicating whether the login was successful, along with a token and its expiration time if successful.
        """

        user = await self.user_repository.get_user_by_email(request.email)
        if not user:
            return LoginResponse(is_successful=False, user_id=None)  # nosec

        user_tries = await self.user_manager_service.validate_user_block(user.id)
        if user_tries.is_blocked:
            return LoginResponse(
                is_successful=False,
                user_id=None,
                is_temporarily_blocked=(
                    user_tries.try_access.is_temporarily_blocked
                    if user_tries and user_tries.try_access
                    else False
                ),
                blocked_until=(
                    user_tries.try_access.temporary_block_expiration
                    if user_tries and user_tries.try_access
                    else 0
                ),
                is_definitively_blocked=(
                    user_tries.try_access.definitively_blocked
                    if user_tries and user_tries.try_access
                    else False
                ),
            )  # nosec

        if not self.password_hasher.verify_password(
            request.password, user.password_hashed
        ):
            increment = await self.user_manager_service.create_fail_try(
                user.id, user_tries.try_access
            )
            return LoginResponse(
                is_successful=False,
                user_id=None,
                is_temporarily_blocked=(
                    increment.is_temporarily_blocked if increment else False
                ),
                blocked_until=increment.temporary_block_expiration if increment else 0,
                is_definitively_blocked=(
                    increment.is_definitively_blocked if increment else False
                ),
            )  # nosec

        otp_generated = await self.user_manager_service.generate_otp(user.id)

        await self.user_repository.reset_login_try_counter(user.id)

        otp_notification_request = UserOTPNotificationRequest(
            email=user.email,
            otp=otp_generated.otp,
            expiration_time=otp_generated.expiration_time,
            username=user.username,
        )
        await self.user_manager_service.send_otp_notification(otp_notification_request)

        return LoginResponse(is_successful=True, user_id=user.id)
