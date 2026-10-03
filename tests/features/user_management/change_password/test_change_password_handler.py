from unittest.mock import Mock, AsyncMock
import pytest

from src.features.user_management.change_password.change_password_handler import (
    ChangePasswordHandler,
)
from src.features.user_management.change_password.change_password_request import (
    ChangePasswordRequestWithToken,
)


@pytest.mark.asyncio
async def test_when_token_is_valid_and_user_exists_then_password_is_changed():

    user_repository = AsyncMock()
    user_recovery_token_repository = AsyncMock()
    password_hasher = Mock()

    user_recover_info = Mock()
    user_recover_info.user_id = "user123"
    user_recover_info.expiration_time = 9999999999
    user_recover_info.token_hashed = "hashed_token"

    user_repository.get_user_by_id = AsyncMock(return_value={"id": "user123"})
    user_recovery_token_repository.get_user_id_by_transaction_id = AsyncMock(
        return_value=user_recover_info
    )
    password_hasher.verify_password = Mock(return_value=True)
    password_hasher.hash_password = Mock(return_value="hashed_new_password")

    new_pass = "NewSecPass123!"
    handler = ChangePasswordHandler(
        user_repository, user_recovery_token_repository, password_hasher
    )
    response = await handler.handle(
        ChangePasswordRequestWithToken(
            token="valid_token", id_trx="valid_id_trx", new_password=new_pass
        )
    )

    assert response.is_success
    assert response.message == "Contraseña cambiada exitosamente"
    user_recovery_token_repository.get_user_id_by_transaction_id.assert_called_once_with(
        "valid_id_trx"
    )
    password_hasher.verify_password.assert_called_once_with(
        "valid_token", "hashed_token"
    )
    user_repository.get_user_by_id.assert_called_once_with("user123")
    user_recovery_token_repository.revoke_tokens_by_user_id.assert_called_once_with(
        "user123"
    )
    password_hasher.hash_password.assert_called_once_with(new_pass)
    user_repository.change_password.assert_called_once_with(
        "user123", "hashed_new_password"
    )


@pytest.mark.asyncio
async def test_when_token_is_invalid_then_should_respond_with_error():

    user_repository = AsyncMock()
    user_recovery_token_repository = AsyncMock()
    password_hasher = Mock()

    user_recover_info = Mock()
    user_recover_info.user_id = "user123"
    user_recover_info.expiration_time = 9999999999
    user_recover_info.token_hashed = "hashed_token"

    user_recovery_token_repository.get_user_id_by_transaction_id = AsyncMock(
        return_value=user_recover_info
    )
    password_hasher.verify_password = Mock(return_value=False)

    new_pass = "NewSecPass123!"
    handler = ChangePasswordHandler(
        user_repository, user_recovery_token_repository, password_hasher
    )
    response = await handler.handle(
        ChangePasswordRequestWithToken(
            token="invalid_token", id_trx="valid_id_trx", new_password=new_pass
        )
    )

    assert not response.is_success
    assert response.message == "Token inválido o expirado"
    user_recovery_token_repository.get_user_id_by_transaction_id.assert_called_once_with(
        "valid_id_trx"
    )
    password_hasher.verify_password.assert_called_once_with(
        "invalid_token", "hashed_token"
    )
    user_repository.get_user_by_id.assert_not_called()
    user_recovery_token_repository.revoke_tokens_by_user_id.assert_not_called()
    password_hasher.hash_password.assert_not_called()
    user_repository.change_password.assert_not_called()


@pytest.mark.asyncio
async def test_when_token_is_expired_then_should_respond_with_error():

    user_repository = AsyncMock()
    user_recovery_token_repository = AsyncMock()
    password_hasher = Mock()

    user_recover_info = Mock()
    user_recover_info.user_id = "user123"
    user_recover_info.expiration_time = 0
    user_recover_info.token_hashed = "hashed_token"

    user_recovery_token_repository.get_user_id_by_transaction_id = AsyncMock(
        return_value=user_recover_info
    )

    new_pass = "NewSecPass123!"
    handler = ChangePasswordHandler(
        user_repository, user_recovery_token_repository, password_hasher
    )
    response = await handler.handle(
        ChangePasswordRequestWithToken(
            token="valid_token", id_trx="valid_id_trx", new_password=new_pass
        )
    )

    assert not response.is_success
    assert response.message == "Token inválido o expirado"
    user_recovery_token_repository.get_user_id_by_transaction_id.assert_called_once_with(
        "valid_id_trx"
    )
    password_hasher.verify_password.assert_not_called()
    user_repository.get_user_by_id.assert_not_called()
    user_recovery_token_repository.revoke_tokens_by_user_id.assert_not_called()
    password_hasher.hash_password.assert_not_called()
    user_repository.change_password.assert_not_called()


@pytest.mark.asyncio
async def test_when_token_is_different_then_should_respond_with_error():

    user_repository = AsyncMock()
    user_recovery_token_repository = AsyncMock()
    password_hasher = Mock()

    user_recover_info = Mock()
    user_recover_info.user_id = "user123"
    user_recover_info.expiration_time = 9999999999
    user_recover_info.token_hashed = "hashed_token"

    user_recovery_token_repository.get_user_id_by_transaction_id = AsyncMock(
        return_value=user_recover_info
    )
    password_hasher.verify_password = Mock(return_value=False)

    new_pass = "NewSecPass123!"
    handler = ChangePasswordHandler(
        user_repository, user_recovery_token_repository, password_hasher
    )
    response = await handler.handle(
        ChangePasswordRequestWithToken(
            token="different_token", id_trx="valid_id_trx", new_password=new_pass
        )
    )

    assert not response.is_success
    assert response.message == "Token inválido o expirado"
    user_recovery_token_repository.get_user_id_by_transaction_id.assert_called_once_with(
        "valid_id_trx"
    )
    password_hasher.verify_password.assert_called_once_with(
        "different_token", "hashed_token"
    )
    user_repository.get_user_by_id.assert_not_called()
    user_recovery_token_repository.revoke_tokens_by_user_id.assert_not_called()
    password_hasher.hash_password.assert_not_called()
    user_repository.change_password.assert_not_called()


@pytest.mark.asyncio
async def test_when_user_does_not_exist_then_should_respond_with_error():
    user_repository = AsyncMock()
    user_recovery_token_repository = AsyncMock()
    password_hasher = Mock()

    user_recover_info = Mock()
    user_recover_info.user_id = "user123"
    user_recover_info.expiration_time = 9999999999
    user_recover_info.token_hashed = "hashed_token"

    user_recovery_token_repository.get_user_id_by_transaction_id = AsyncMock(
        return_value=user_recover_info
    )
    password_hasher.verify_password = Mock(return_value=True)
    user_repository.get_user_by_id = AsyncMock(return_value=None)

    new_pass = "NewSecPass123!"
    handler = ChangePasswordHandler(
        user_repository, user_recovery_token_repository, password_hasher
    )
    response = await handler.handle(
        ChangePasswordRequestWithToken(
            token="valid_token", id_trx="valid_id_trx", new_password=new_pass
        )
    )

    assert not response.is_success
    assert response.message == "Usuario no encontrado"
    user_recovery_token_repository.get_user_id_by_transaction_id.assert_called_once_with(
        "valid_id_trx"
    )
    password_hasher.verify_password.assert_called_once_with(
        "valid_token", "hashed_token"
    )
    user_repository.get_user_by_id.assert_called_once_with("user123")
    user_recovery_token_repository.revoke_tokens_by_user_id.assert_not_called()
    password_hasher.hash_password.assert_not_called()
    user_repository.change_password.assert_not_called()
