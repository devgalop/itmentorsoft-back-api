from common_py_aws import PublisherService

from src.infrastructure.notification.notification_message import (
    NotificationMessage,
    NotificationMessageVariables,
    NotificationResponse,
    OtpNotifyRequest,
    QuestionCreatedNotifyRequest,
    RecoverPasswordNotifyRequest,
    UserCreatedNotifyRequest,
)


class NotificatorService:

    DEFAULT_ERROR_MESSAGE = "Fallo al enviar la notificación"
    DEFAULT_SUCCESS_MESSAGE = "Notificación enviada con éxito"

    def __init__(
        self,
        publisher_service: PublisherService,
    ):
        self.publisher_service = publisher_service

    async def send_otp_notification(
        self, request: OtpNotifyRequest
    ) -> NotificationResponse:
        """Send OTP notification to the user.

        Args:
            request (OtpNotifyRequest): The request object containing OTP notification details.

        Returns:
            NotificationResponse: The response indicating the success or failure of the notification.
        """
        try:
            response = await self.publisher_service.publish(
                NotificationMessage(
                    recipient=request.recipient,
                    subject="Código temporal de acceso",
                    html_template_code="otp",
                    message_variables=[
                        NotificationMessageVariables(key="%USER%", value=request.user),
                        NotificationMessageVariables(
                            key="%OTP_CODE%", value=request.otp_code
                        ),
                        NotificationMessageVariables(
                            key="%OTP_EXPIRATION_MINUTES%", value=request.expiration
                        ),
                    ],
                )
            )
            if not response:
                return NotificationResponse(
                    is_success=False, message=self.DEFAULT_ERROR_MESSAGE
                )

            return NotificationResponse(
                is_success=True, message=self.DEFAULT_SUCCESS_MESSAGE
            )
        except Exception as e:
            return NotificationResponse(is_success=False, message=str(e))

    async def send_question_created_notification(
        self, request: QuestionCreatedNotifyRequest
    ) -> NotificationResponse:
        """Send notification when a new question is created.

        Args:
            request (QuestionCreatedNotifyRequest): The request object containing question creation notification details.

        Returns:
            NotificationResponse: The response indicating the success or failure of the notification.
        """
        try:
            response = await self.publisher_service.publish(
                NotificationMessage(
                    recipient=request.recipient,
                    subject="Ha sido creada una nueva pregunta",
                    html_template_code="item_created",
                    message_variables=[
                        NotificationMessageVariables(
                            key="%REVIEWER%", value=request.reviewer
                        ),
                        NotificationMessageVariables(
                            key="%CREATED_BY%", value=request.owner
                        ),
                        NotificationMessageVariables(
                            key="%OBJECT_NAME%", value=request.object_name
                        ),
                        NotificationMessageVariables(
                            key="%OBJECT_CODE%", value=request.object_code
                        ),
                        NotificationMessageVariables(
                            key="%CREATED_DATE%", value=request.created_at
                        ),
                        NotificationMessageVariables(
                            key="%URL_REVIEW%", value=request.url_review
                        ),
                    ],
                )
            )
            if not response:
                return NotificationResponse(
                    is_success=False, message=self.DEFAULT_ERROR_MESSAGE
                )

            return NotificationResponse(
                is_success=True, message=self.DEFAULT_SUCCESS_MESSAGE
            )
        except Exception as e:
            return NotificationResponse(is_success=False, message=str(e))

    async def send_recovery_notification(
        self, request: RecoverPasswordNotifyRequest
    ) -> NotificationResponse:
        """Send Recovery Password Notification.

        Args:
            request (RecoverPasswordNotifyRequest): The request containing the details for the recovery password notification.

        Returns:
            NotificationResponse: The response indicating the success or failure of the recovery password notification.
        """
        try:
            response = await self.publisher_service.publish(
                NotificationMessage(
                    recipient=request.recipient,
                    subject="Solicitud de recuperación de contraseña",
                    html_template_code="recovery_password",
                    message_variables=[
                        NotificationMessageVariables(
                            key="%URL_BASE%", value=request.url_base
                        ),
                        NotificationMessageVariables(
                            key="%URL_TOKEN%", value=request.url_token
                        ),
                        NotificationMessageVariables(key="%USER%", value=request.user),
                        NotificationMessageVariables(
                            key="%ID_TRX%", value=request.id_trx
                        ),
                    ],
                )
            )
            if not response:
                return NotificationResponse(
                    is_success=False, message=self.DEFAULT_ERROR_MESSAGE
                )

            return NotificationResponse(
                is_success=True, message=self.DEFAULT_SUCCESS_MESSAGE
            )
        except Exception as e:
            return NotificationResponse(is_success=False, message=str(e))

    async def send_user_created_notification(
        self, request: UserCreatedNotifyRequest
    ) -> NotificationResponse:
        try:
            response = await self.publisher_service.publish(
                NotificationMessage(
                    recipient=request.recipient,
                    subject="Se ha registrado un nuevo usuario",
                    html_template_code="user_created",
                    message_variables=[
                        NotificationMessageVariables(key="%USER%", value=request.user),
                        NotificationMessageVariables(
                            key="%EMAIL%", value=request.recipient
                        ),
                        NotificationMessageVariables(key="%ROLE%", value=request.role),
                        NotificationMessageVariables(
                            key="%REGISTER_DATE%", value=request.created_at
                        ),
                        NotificationMessageVariables(
                            key="%LOGIN_URL%", value=request.login_url
                        ),
                    ],
                )
            )
            if not response:
                return NotificationResponse(
                    is_success=False, message=self.DEFAULT_ERROR_MESSAGE
                )

            return NotificationResponse(
                is_success=True, message=self.DEFAULT_SUCCESS_MESSAGE
            )
        except Exception as e:
            return NotificationResponse(is_success=False, message=str(e))
