import pytest

from src.features.user_management.login.login_request import LoginRequest

GENERIC_ERROR_MESSAGE_LOGIN = "Invalid email or password"


def test_when_request_is_valid_should_not_raise_exception():
    sample_pass = "Example123*"
    request = LoginRequest(email="test@example.com", password=sample_pass)
    assert request.email == "test@example.com"
    assert request.password == sample_pass


def test_when_email_is_invalid_should_raise_exception():
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="invalid-email", password="securepassword")


def test_when_email_is_missing_should_raise_exception():
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="", password="securepassword")


def test_when_email_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="a@b", password="securepassword")


def test_when_email_is_too_long_should_raise_exception():
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="a" * 256 + "@example.com", password="securepassword")


def test_when_password_is_missing_should_raise_exception():
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="test@example.com", password="")


def test_when_password_is_too_short_should_raise_exception():
    short_pass = "short"
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="test@example.com", password=short_pass)


def test_when_password_is_too_long_should_raise_exception():
    long_pass = "a" * 21
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="test@example.com", password=long_pass)


def test_when_password_has_no_digits_should_raise_exception():
    no_digits = "NoDigitsHere!"
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="test@example.com", password=no_digits)


def test_when_password_has_no_letters_should_raise_exception():
    no_letters = "12345678!"
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="test@example.com", password=no_letters)


def test_when_password_has_no_special_characters_should_raise_exception():
    no_special = "Password123"
    with pytest.raises(ValueError, match=GENERIC_ERROR_MESSAGE_LOGIN):
        LoginRequest(email="test@example.com", password=no_special)
