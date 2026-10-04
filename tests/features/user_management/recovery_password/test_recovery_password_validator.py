from src.features.user_management.recovery_password.recovery_password_request import (
    RecoveryPasswordRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = RecoveryPasswordRequest(email="test@example.com")
    assert request.email == "test@example.com"


def test_when_email_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email es requerido"):
        RecoveryPasswordRequest(email="")


def test_when_email_is_invalid_then_exception_is_raised():
    with pytest.raises(ValueError, match="Formato de email inválido"):
        RecoveryPasswordRequest(email="invalid-email")


def test_when_email_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email no debe exceder 255 caracteres"):
        RecoveryPasswordRequest(email="a" * 256 + "@example.com")


def test_when_email_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email debe tener al menos 5 caracteres"):
        RecoveryPasswordRequest(email="a@b")
