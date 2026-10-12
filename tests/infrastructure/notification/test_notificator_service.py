from unittest.mock import AsyncMock, MagicMock

import pytest

from src.infrastructure.notification.notification_message import (
    NotificationMessage,
    OtpNotifyRequest,
    QuestionCreatedNotifyRequest,
    RecoverPasswordNotifyRequest,
    UserCreatedNotifyRequest,
)
from src.infrastructure.notification.notificator_service import NotificatorService


@pytest.fixture
def mock_publisher_service():
    """Create a mocked PublisherService."""
    return MagicMock()


@pytest.fixture
def service(mock_publisher_service):
    """Create NotificatorService with mocked PublisherService."""
    return NotificatorService(publisher_service=mock_publisher_service)


class TestSendOtpNotification:
    """Tests for NotificatorService.send_otp_notification."""

    @pytest.mark.asyncio
    async def test_success_when_publish_returns_truthy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid OtpNotifyRequest
        WHEN send_otp_notification is called and publish returns truthy
        THEN returns success NotificationResponse.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = OtpNotifyRequest(
            recipient="user@example.com",
            user="testuser",
            otp_code="123456",
            expiration="10",
        )

        result = await service.send_otp_notification(request)

        assert result.is_success is True
        assert result.message == NotificatorService.DEFAULT_SUCCESS_MESSAGE
        mock_publisher_service.publish.assert_called_once()
        self._assert_notification_message(
            mock_publisher_service.publish.call_args[0][0],
            recipient="user@example.com",
            subject="Código temporal de acceso",
            html_template_code="otp",
        )

    @pytest.mark.asyncio
    async def test_failure_when_publish_returns_falsy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid OtpNotifyRequest
        WHEN send_otp_notification is called and publish returns falsy (None)
        THEN returns failure NotificationResponse with default error message.
        """
        mock_publisher_service.publish = AsyncMock(return_value=None)
        request = OtpNotifyRequest(
            recipient="user@example.com",
            user="testuser",
            otp_code="123456",
            expiration="10",
        )

        result = await service.send_otp_notification(request)

        assert result.is_success is False
        assert result.message == NotificatorService.DEFAULT_ERROR_MESSAGE

    @pytest.mark.asyncio
    async def test_failure_when_publish_raises_exception(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid OtpNotifyRequest
        WHEN send_otp_notification is called and publish raises an exception
        THEN returns failure NotificationResponse with exception message.
        """
        mock_publisher_service.publish = AsyncMock(
            side_effect=RuntimeError("Connection timeout")
        )
        request = OtpNotifyRequest(
            recipient="user@example.com",
            user="testuser",
            otp_code="123456",
            expiration="10",
        )

        result = await service.send_otp_notification(request)

        assert result.is_success is False
        assert result.message == "Connection timeout"

    @pytest.mark.asyncio
    async def test_message_variables_contain_expected_keys(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid OtpNotifyRequest
        WHEN send_otp_notification is called
        THEN NotificationMessage contains %USER%, %OTP_CODE%, and %OTP_EXPIRATION_MINUTES% variables.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = OtpNotifyRequest(
            recipient="user@example.com",
            user="testuser",
            otp_code="654321",
            expiration="5",
        )

        await service.send_otp_notification(request)

        msg: NotificationMessage = mock_publisher_service.publish.call_args[0][0]
        var_keys = [v.key for v in msg.message_variables]
        assert "%USER%" in var_keys
        assert "%OTP_CODE%" in var_keys
        assert "%OTP_EXPIRATION_MINUTES%" in var_keys

        var_dict = {v.key: v.value for v in msg.message_variables}
        assert var_dict["%USER%"] == "testuser"
        assert var_dict["%OTP_CODE%"] == "654321"
        assert var_dict["%OTP_EXPIRATION_MINUTES%"] == "5"

    @staticmethod
    def _assert_notification_message(msg, recipient, subject, html_template_code):
        assert msg.recipient == recipient
        assert msg.subject == subject
        assert msg.html_template_code == html_template_code


class TestSendQuestionCreatedNotification:
    """Tests for NotificatorService.send_question_created_notification."""

    @pytest.mark.asyncio
    async def test_success_when_publish_returns_truthy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid QuestionCreatedNotifyRequest
        WHEN send_question_created_notification is called and publish returns truthy
        THEN returns success NotificationResponse.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = QuestionCreatedNotifyRequest(
            recipient="reviewer@example.com",
            reviewer="Dr. Smith",
            owner="John Doe",
            object_name="Python Basics",
            object_code="PY-001",
            created_at="2026-10-12",
            url_review="https://example.com/review/1",
        )

        result = await service.send_question_created_notification(request)

        assert result.is_success is True
        assert result.message == NotificatorService.DEFAULT_SUCCESS_MESSAGE
        mock_publisher_service.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_failure_when_publish_returns_falsy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid QuestionCreatedNotifyRequest
        WHEN send_question_created_notification is called and publish returns falsy
        THEN returns failure NotificationResponse with default error message.
        """
        mock_publisher_service.publish = AsyncMock(return_value=None)
        request = QuestionCreatedNotifyRequest(
            recipient="reviewer@example.com",
            reviewer="Dr. Smith",
            owner="John Doe",
            object_name="Python Basics",
            object_code="PY-001",
            created_at="2026-10-12",
            url_review="https://example.com/review/1",
        )

        result = await service.send_question_created_notification(request)

        assert result.is_success is False
        assert result.message == NotificatorService.DEFAULT_ERROR_MESSAGE

    @pytest.mark.asyncio
    async def test_failure_when_publish_raises_exception(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid QuestionCreatedNotifyRequest
        WHEN send_question_created_notification is called and publish raises an exception
        THEN returns failure NotificationResponse with exception message.
        """
        mock_publisher_service.publish = AsyncMock(
            side_effect=ConnectionError("SQS unreachable")
        )
        request = QuestionCreatedNotifyRequest(
            recipient="reviewer@example.com",
            reviewer="Dr. Smith",
            owner="John Doe",
            object_name="Python Basics",
            object_code="PY-001",
            created_at="2026-10-12",
            url_review="https://example.com/review/1",
        )

        result = await service.send_question_created_notification(request)

        assert result.is_success is False
        assert result.message == "SQS unreachable"

    @pytest.mark.asyncio
    async def test_message_variables_contain_expected_keys(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid QuestionCreatedNotifyRequest
        WHEN send_question_created_notification is called
        THEN NotificationMessage contains all expected template variables.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = QuestionCreatedNotifyRequest(
            recipient="reviewer@example.com",
            reviewer="Dr. Smith",
            owner="John Doe",
            object_name="Python Basics",
            object_code="PY-001",
            created_at="2026-10-12",
            url_review="https://example.com/review/1",
        )

        await service.send_question_created_notification(request)

        msg: NotificationMessage = mock_publisher_service.publish.call_args[0][0]
        var_keys = [v.key for v in msg.message_variables]
        expected_keys = [
            "%REVIEWER%",
            "%CREATED_BY%",
            "%OBJECT_NAME%",
            "%OBJECT_CODE%",
            "%CREATED_DATE%",
            "%URL_REVIEW%",
        ]
        for key in expected_keys:
            assert key in var_keys

        assert msg.subject == "Ha sido creada una nueva pregunta"
        assert msg.html_template_code == "item_created"


class TestSendRecoveryNotification:
    """Tests for NotificatorService.send_recovery_notification."""

    @pytest.mark.asyncio
    async def test_success_when_publish_returns_truthy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid RecoverPasswordNotifyRequest
        WHEN send_recovery_notification is called and publish returns truthy
        THEN returns success NotificationResponse.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = RecoverPasswordNotifyRequest(
            recipient="user@example.com",
            url_base="https://example.com",
            url_token="abc123",
            user="testuser",
            id_trx="TRX-001",
        )

        result = await service.send_recovery_notification(request)

        assert result.is_success is True
        assert result.message == NotificatorService.DEFAULT_SUCCESS_MESSAGE
        mock_publisher_service.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_failure_when_publish_returns_falsy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid RecoverPasswordNotifyRequest
        WHEN send_recovery_notification is called and publish returns falsy
        THEN returns failure NotificationResponse with default error message.
        """
        mock_publisher_service.publish = AsyncMock(return_value=None)
        request = RecoverPasswordNotifyRequest(
            recipient="user@example.com",
            url_base="https://example.com",
            url_token="abc123",
            user="testuser",
            id_trx="TRX-001",
        )

        result = await service.send_recovery_notification(request)

        assert result.is_success is False
        assert result.message == NotificatorService.DEFAULT_ERROR_MESSAGE

    @pytest.mark.asyncio
    async def test_failure_when_publish_raises_exception(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid RecoverPasswordNotifyRequest
        WHEN send_recovery_notification is called and publish raises an exception
        THEN returns failure NotificationResponse with exception message.
        """
        mock_publisher_service.publish = AsyncMock(
            side_effect=ValueError("Invalid token")
        )
        request = RecoverPasswordNotifyRequest(
            recipient="user@example.com",
            url_base="https://example.com",
            url_token="abc123",
            user="testuser",
            id_trx="TRX-001",
        )

        result = await service.send_recovery_notification(request)

        assert result.is_success is False
        assert result.message == "Invalid token"

    @pytest.mark.asyncio
    async def test_message_variables_contain_expected_keys(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid RecoverPasswordNotifyRequest
        WHEN send_recovery_notification is called
        THEN NotificationMessage contains all expected template variables.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = RecoverPasswordNotifyRequest(
            recipient="user@example.com",
            url_base="https://example.com",
            url_token="abc123",
            user="testuser",
            id_trx="TRX-001",
        )

        await service.send_recovery_notification(request)

        msg: NotificationMessage = mock_publisher_service.publish.call_args[0][0]
        var_keys = [v.key for v in msg.message_variables]
        expected_keys = ["%URL_BASE%", "%URL_TOKEN%", "%USER%", "%ID_TRX%"]
        for key in expected_keys:
            assert key in var_keys

        assert msg.subject == "Solicitud de recuperación de contraseña"
        assert msg.html_template_code == "recovery_password"


class TestSendUserCreatedNotification:
    """Tests for NotificatorService.send_user_created_notification."""

    @pytest.mark.asyncio
    async def test_success_when_publish_returns_truthy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid UserCreatedNotifyRequest
        WHEN send_user_created_notification is called and publish returns truthy
        THEN returns success NotificationResponse.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = UserCreatedNotifyRequest(
            recipient="newuser@example.com",
            user="newuser",
            role="student",
            created_at="2026-10-12",
            login_url="https://example.com/login",
        )

        result = await service.send_user_created_notification(request)

        assert result.is_success is True
        assert result.message == NotificatorService.DEFAULT_SUCCESS_MESSAGE
        mock_publisher_service.publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_failure_when_publish_returns_falsy(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid UserCreatedNotifyRequest
        WHEN send_user_created_notification is called and publish returns falsy
        THEN returns failure NotificationResponse with default error message.
        """
        mock_publisher_service.publish = AsyncMock(return_value=None)
        request = UserCreatedNotifyRequest(
            recipient="newuser@example.com",
            user="newuser",
            role="student",
            created_at="2026-10-12",
            login_url="https://example.com/login",
        )

        result = await service.send_user_created_notification(request)

        assert result.is_success is False
        assert result.message == NotificatorService.DEFAULT_ERROR_MESSAGE

    @pytest.mark.asyncio
    async def test_failure_when_publish_raises_exception(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid UserCreatedNotifyRequest
        WHEN send_user_created_notification is called and publish raises an exception
        THEN returns failure NotificationResponse with exception message.
        """
        mock_publisher_service.publish = AsyncMock(
            side_effect=TimeoutError("Queue timeout")
        )
        request = UserCreatedNotifyRequest(
            recipient="newuser@example.com",
            user="newuser",
            role="student",
            created_at="2026-10-12",
            login_url="https://example.com/login",
        )

        result = await service.send_user_created_notification(request)

        assert result.is_success is False
        assert result.message == "Queue timeout"

    @pytest.mark.asyncio
    async def test_message_variables_contain_expected_keys(
        self, service, mock_publisher_service
    ):
        """GIVEN a valid UserCreatedNotifyRequest
        WHEN send_user_created_notification is called
        THEN NotificationMessage contains all expected template variables.
        """
        mock_publisher_service.publish = AsyncMock(return_value=True)
        request = UserCreatedNotifyRequest(
            recipient="newuser@example.com",
            user="newuser",
            role="admin",
            created_at="2026-10-12",
            login_url="https://example.com/login",
        )

        await service.send_user_created_notification(request)

        msg: NotificationMessage = mock_publisher_service.publish.call_args[0][0]
        var_keys = [v.key for v in msg.message_variables]
        expected_keys = [
            "%USER%",
            "%EMAIL%",
            "%ROLE%",
            "%REGISTER_DATE%",
            "%LOGIN_URL%",
        ]
        for key in expected_keys:
            assert key in var_keys

        assert msg.subject == "Se ha registrado un nuevo usuario"
        assert msg.html_template_code == "user_created"
        var_dict = {v.key: v.value for v in msg.message_variables}
        assert var_dict["%USER%"] == "newuser"
        assert var_dict["%EMAIL%"] == "newuser@example.com"
        assert var_dict["%ROLE%"] == "admin"


class TestNotificatorServiceInit:
    """Tests for NotificatorService constructor and class attributes."""

    def test_default_error_message(self):
        """GIVEN the NotificatorService class
        WHEN accessing DEFAULT_ERROR_MESSAGE
        THEN it returns the expected error message.
        """
        assert (
            NotificatorService.DEFAULT_ERROR_MESSAGE
            == "Fallo al enviar la notificación"
        )

    def test_default_success_message(self):
        """GIVEN the NotificatorService class
        WHEN accessing DEFAULT_SUCCESS_MESSAGE
        THEN it returns the expected success message.
        """
        assert (
            NotificatorService.DEFAULT_SUCCESS_MESSAGE
            == "Notificación enviada con éxito"
        )

    def test_service_stores_publisher_dependency(self, mock_publisher_service):
        """GIVEN a PublisherService instance
        WHEN NotificatorService is instantiated
        THEN the publisher_service is stored as an attribute.
        """
        service = NotificatorService(publisher_service=mock_publisher_service)
        assert service.publisher_service is mock_publisher_service
