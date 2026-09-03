from unittest.mock import Mock, AsyncMock
import pytest

from src.features.user_management.login.login_handler import LoginHandler
from src.features.user_management.login.login_request import LoginRequest
from src.features.user_management.shared.token_generator import TokenResponse
from itmentorsoft_persistence.dto import (
    CompleteUserResponse,
    UserRole,
    UserStatus,
)


@pytest.mark.asyncio
async def test_when_credentials_are_valid_should_login_user():
    user_repository = AsyncMock()
    password_hasher = Mock()
    token_generator = Mock()
    refresh_token_repository = AsyncMock()

    user_repository.get_user_by_email = AsyncMock(
        return_value=CompleteUserResponse(
            id="user_id",
            username="testuser",
            email="test@example.com",
            password_hashed="hashed_password",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )
    password_hasher.verify_password = Mock(return_value=True)
    token_generator.generate_token = Mock(
        return_value=TokenResponse(token="jwt_token", expiration_time=3600)
    )
    token_generator.generate_random_token = Mock(
        return_value=TokenResponse(token="refresh_raw", expiration_time=9999)
    )
    password_hasher.hash_password = Mock(return_value="hashed_refresh")
    refresh_token_repository.save_token = AsyncMock()

    handler = LoginHandler(
        user_repository, password_hasher, token_generator, refresh_token_repository
    )
    sample_pass = "Password123!"
    response = await handler.handle(
        LoginRequest(email="test@example.com", password=sample_pass)
    )
    assert response.is_successful
    assert response.token == "jwt_token"
    user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    password_hasher.verify_password.assert_called_once_with(
        sample_pass, "hashed_password"
    )
    token_generator.generate_token.assert_called_once()


@pytest.mark.asyncio
async def test_when_email_does_not_exist_should_return_empty_response():
    user_repository = AsyncMock()
    password_hasher = Mock()
    token_generator = Mock()
    refresh_token_repository = AsyncMock()

    user_repository.get_user_by_email = AsyncMock(return_value=None)

    handler = LoginHandler(
        user_repository, password_hasher, token_generator, refresh_token_repository
    )
    response = await handler.handle(
        LoginRequest(email="invalid@example.com", password="Password123!")
    )

    assert not response.is_successful
    assert response.token == ""
    assert response.expiration_time == 0
    user_repository.get_user_by_email.assert_called_once_with("invalid@example.com")
    password_hasher.verify_password.assert_not_called()
    token_generator.generate_token.assert_not_called()


@pytest.mark.asyncio
async def test_when_password_is_incorrect_should_return_empty_response():
    user_repository = AsyncMock()
    password_hasher = Mock()
    token_generator = Mock()
    refresh_token_repository = AsyncMock()

    user_repository.get_user_by_email = AsyncMock(
        return_value=CompleteUserResponse(
            id="user_id",
            username="testuser",
            email="test@example.com",
            password_hashed="hashed_password",
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
    )
    password_hasher.verify_password = Mock(return_value=False)

    handler = LoginHandler(
        user_repository, password_hasher, token_generator, refresh_token_repository
    )
    response = await handler.handle(
        LoginRequest(email="test@example.com", password="IncorrectPassword12!")
    )

    assert not response.is_successful
    assert response.token == ""
    assert response.expiration_time == 0
    user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    password_hasher.verify_password.assert_called_once_with(
        "IncorrectPassword12!", "hashed_password"
    )
    token_generator.generate_token.assert_not_called()
