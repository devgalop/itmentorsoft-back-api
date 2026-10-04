from src.features.user_management.create_user_from_admin.create_user_from_admin_request import (
    CreateUserFromAdminRequest,
)
import pytest


def test_when_request_is_valid_then_no_exception_is_raised():
    request = CreateUserFromAdminRequest(
        email="test@example.com", username="testuser", role="student", name="Test User"
    )
    assert request.email == "test@example.com"
    assert request.username == "testuser"
    assert request.role == "student"


def test_when_email_is_invalid_then_exception_is_raised():
    with pytest.raises(ValueError, match="Formato de email inválido"):
        CreateUserFromAdminRequest(
            email="invalid-email", username="testuser", role="student", name="Test User"
        )


def test_when_email_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email es requerido"):
        CreateUserFromAdminRequest(
            email="", username="testuser", role="student", name="Test User"
        )


def test_when_email_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email debe tener al menos 5 caracteres"):
        CreateUserFromAdminRequest(
            email="a@b", username="testuser", role="student", name="Test User"
        )


def test_when_email_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email no debe exceder 255 caracteres"):
        CreateUserFromAdminRequest(
            email="a" * 256 + "@example.com",
            username="testuser",
            role="student",
            name="Test User",
        )


def test_when_username_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Nombre de usuario es requerido"):
        CreateUserFromAdminRequest(
            email="test@example.com", username="", role="student", name="Test User"
        )


def test_when_username_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Nombre de usuario debe tener al menos 3 caracteres"
    ):
        CreateUserFromAdminRequest(
            email="test@example.com", username="ab", role="student", name="Test User"
        )


def test_when_username_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Nombre de usuario no debe exceder 20 caracteres"
    ):
        CreateUserFromAdminRequest(
            email="test@example.com",
            username="a" * 21,
            role="student",
            name="Test User",
        )


def test_when_username_has_invalid_characters_then_exception_is_raised():
    with pytest.raises(ValueError):
        CreateUserFromAdminRequest(
            email="test@example.com",
            username="invalid$username",
            role="student",
            name="Test User",
        )


def test_when_role_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Role is required"):
        CreateUserFromAdminRequest(
            email="test@example.com", username="testuser", role="", name="Test User"
        )


def test_when_role_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Rol debe tener al menos 3 caracteres"):
        CreateUserFromAdminRequest(
            email="test@example.com", username="testuser", role="ab", name="Test User"
        )


def test_when_role_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Rol no debe exceder 20 caracteres"):
        CreateUserFromAdminRequest(
            email="test@example.com",
            username="testuser",
            role="a" * 21,
            name="Test User",
        )
