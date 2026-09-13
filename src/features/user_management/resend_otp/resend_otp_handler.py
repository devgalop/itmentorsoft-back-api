from itmentorsoft_persistence import UserRepository

from src.features.user_management.resend_otp.resend_otp_request import ResendOtpRequest
from src.features.user_management.resend_otp.resend_otp_response import (
    ResendOTPResponse,
)
from src.features.user_management.shared.user_manager_service import (
    UserManagerService,
    UserOTPNotificationRequest,
)


class ResendOTPHandler:
    GENERIC_OTP_MESSAGE = (
        "If your account exists, an OTP has been sent to your registered email."
    )

    def __init__(
        self, user_repository: UserRepository, user_manager_service: UserManagerService
    ):
        self.user_repository = user_repository
        self.user_manager_service = user_manager_service

    async def handle(self, request: ResendOtpRequest) -> ResendOTPResponse:
        user = await self.user_repository.get_user_by_id(request.user_id)
        if not user:
            return ResendOTPResponse(message=self.GENERIC_OTP_MESSAGE)

        user_tries = await self.user_manager_service.validate_user_block(user.id)
        if user_tries.is_blocked:
            return ResendOTPResponse(message=self.GENERIC_OTP_MESSAGE)

        increment = await self.user_manager_service.create_fail_try(
            user.id, user_tries.try_access
        )
        if increment.is_definitively_blocked:
            return ResendOTPResponse(message=self.GENERIC_OTP_MESSAGE)

        otp_result = await self.user_manager_service.generate_otp(
            user_id=request.user_id
        )

        otp_notification_request = UserOTPNotificationRequest(
            email=user.email,
            otp=otp_result.otp,
            expiration_time=otp_result.expiration_time,
            username=user.username,
        )
        await self.user_manager_service.send_otp_notification(otp_notification_request)

        return ResendOTPResponse(message=self.GENERIC_OTP_MESSAGE)
