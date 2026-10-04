from src.features.user_management.change_password.change_password_request import (
    ChangePasswordRequest,
    ChangePasswordRequestWithToken,
)
import pytest


def test_when_token_is_valid_and_new_password_is_provided_then_no_validation_errors():
    new_pass = "NewSecPass123!"
    request = ChangePasswordRequest(new_password=new_pass)
    token = "valid_token"
    id_trx = "valid_id_trx"
    change_password_request = ChangePasswordRequestWithToken(
        token=token, id_trx=id_trx, new_password=request.new_password
    )
    assert change_password_request.token == token
    assert change_password_request.id_trx == id_trx
    assert change_password_request.new_password == new_pass


def test_when_token_is_missing_then_validation_error():
    new_pass = "NewSecPass123!"
    request = ChangePasswordRequest(new_password=new_pass)
    token = ""
    id_trx = "valid_id_trx"
    with pytest.raises(ValueError, match="Token is required"):
        ChangePasswordRequestWithToken(
            token=token, id_trx=id_trx, new_password=request.new_password
        )


def test_when_id_trx_is_missing_then_validation_error():
    new_pass = "NewSecPass123!"
    request = ChangePasswordRequest(new_password=new_pass)
    token = "valid_token"
    id_trx = ""
    with pytest.raises(ValueError, match="Transaction ID is required"):
        ChangePasswordRequestWithToken(
            token=token, id_trx=id_trx, new_password=request.new_password
        )


def test_when_new_password_is_missing_then_validation_error():
    with pytest.raises(ValueError, match="Contraseña es requerida"):
        ChangePasswordRequest(new_password="")


def test_when_new_password_is_too_short_then_validation_error():
    new_pass = "Ab1!"
    with pytest.raises(ValueError, match="Contraseña debe tener al menos 6 caracteres"):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_is_too_long_then_validation_error():
    new_pass = "A" * 21 + "1!"
    with pytest.raises(ValueError, match="Contraseña no debe exceder 20 caracteres"):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_has_no_digit_then_validation_error():
    new_pass = "NewSecPass!"
    with pytest.raises(ValueError, match="Contraseña debe contener al menos un dígito"):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_has_no_letter_then_validation_error():
    new_pass = "12345678!"
    with pytest.raises(ValueError, match="Contraseña debe contener al menos una letra"):
        ChangePasswordRequest(new_password=new_pass)


def test_when_new_password_has_no_special_char_then_validation_error():
    new_pass = "NewSecPass123"
    with pytest.raises(
        ValueError, match="Contraseña debe contener al menos un carácter especial"
    ):
        ChangePasswordRequest(new_password=new_pass)


def test_when_token_is_too_short_then_validation_error():
    new_pass = "NewSecPass123!"
    with pytest.raises(ValueError, match="Token must be at least 5 characters long"):
        ChangePasswordRequestWithToken(
            token="ab",  # len 2 < 5
            id_trx="valid_id_trx",
            new_password=new_pass,
        )


def test_when_token_is_too_long_then_validation_error():
    new_pass = "NewSecPass123!"
    with pytest.raises(
        ValueError, match="Token must be no more than 255 characters long"
    ):
        ChangePasswordRequestWithToken(
            token="a" * 256,  # len 256 > 255
            id_trx="valid_id_trx",
            new_password=new_pass,
        )


def test_when_id_trx_is_too_short_then_validation_error():
    new_pass = "NewSecPass123!"
    with pytest.raises(
        ValueError, match="Transaction ID must be at least 5 characters long"
    ):
        ChangePasswordRequestWithToken(
            token="valid_token",
            id_trx="ab",  # len 2 < 5
            new_password=new_pass,
        )


def test_when_id_trx_is_too_long_then_validation_error():
    new_pass = "NewSecPass123!"
    with pytest.raises(
        ValueError, match="Transaction ID must be no more than 255 characters long"
    ):
        ChangePasswordRequestWithToken(
            token="valid_token",
            id_trx="a" * 256,  # len 256 > 255
            new_password=new_pass,
        )
