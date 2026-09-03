from unittest.mock import AsyncMock
import pytest

from src.features.user_management.recovery_password.recovery_password_handler import (
    RecoveryPasswordHandler,
)
from src.features.user_management.recovery_password.recovery_password_request import (
    RecoveryPasswordRequest,
)
from src.features.user_management.recovery_password.recovery_password_response import (
    RecoveryPasswordResponse,
)
from src.features.shared.notification_service import NotificationService
from src.features.shared.template_loader import TemplateLoader
from src.features.user_management.shared.token_generator import TokenGenerator
from src.features.user_management.shared.password_hasher import PasswordHasher
from itmentorsoft_persistence.repositories import UserRecoveryTokenRepository
from itmentorsoft_persistence.repositories import UserRepository


@pytest.mark.asyncio
async def test_when_email_does_not_exist_then_response_message_is_returned():
    user_repository = AsyncMock(spec=UserRepository)
    user_repository.get_user_response_by_email.return_value = None
    token_generator = AsyncMock(spec=TokenGenerator)
    user_recovery_repository = AsyncMock(spec=UserRecoveryTokenRepository)
    notification_service = AsyncMock(spec=NotificationService)
    password_hasher = AsyncMock(spec=PasswordHasher)
    template_loader = TemplateLoader()

    handler = RecoveryPasswordHandler(
        user_repository=user_repository,
        user_recovery_token_repository=user_recovery_repository,
        notification_service=notification_service,
        token_generator=token_generator,
        password_hasher=password_hasher,
        template_loader=template_loader,
    )

    request = RecoveryPasswordRequest(email="nonexistent@example.com")
    response = await handler.handle(request)

    assert isinstance(response, RecoveryPasswordResponse)
    assert (
        response.message
        == "If the email exists in our system, you will receive a password recovery email shortly."
    )
    user_repository.get_user_response_by_email.assert_called_once_with(
        "nonexistent@example.com"
    )
    token_generator.generate_random_token.assert_not_called()
    password_hasher.hash_password.assert_not_called()
    notification_service.send_notification.assert_not_called()
    user_recovery_repository.save_token.assert_not_called()


@pytest.mark.asyncio
async def test_when_email_exists_then_recovery_process_is_initiated():
    user_repository = AsyncMock(spec=UserRepository)
    user_repository.get_user_response_by_email.return_value = AsyncMock(
        id=1, username="testuser"
    )
    token_generator = AsyncMock(spec=TokenGenerator)
    token_generator.generate_random_token.return_value = AsyncMock(
        token="random-token", expiration_time=1234567890
    )
    user_recovery_repository = AsyncMock(spec=UserRecoveryTokenRepository)
    notification_service = AsyncMock(spec=NotificationService)
    password_hasher = AsyncMock(spec=PasswordHasher)
    password_hasher.hash_password.return_value = "hashed-token"
    template_loader = TemplateLoader()

    handler = RecoveryPasswordHandler(
        user_repository=user_repository,
        user_recovery_token_repository=user_recovery_repository,
        notification_service=notification_service,
        token_generator=token_generator,
        password_hasher=password_hasher,
        template_loader=template_loader,
    )

    request = RecoveryPasswordRequest(email="testuser@example.com")
    response = await handler.handle(request)

    assert isinstance(response, RecoveryPasswordResponse)
    assert (
        response.message
        == "If the email exists in our system, you will receive a password recovery email shortly."
    )
    user_repository.get_user_response_by_email.assert_called_once_with(
        "testuser@example.com"
    )
    token_generator.generate_random_token.assert_called_once()
    password_hasher.hash_password.assert_called_once_with("random-token")
    notification_service.send_notification.assert_called_once()
    user_recovery_repository.save_token.assert_called_once()
