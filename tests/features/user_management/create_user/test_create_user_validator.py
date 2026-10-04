from src.features.user_management.create_user.create_user_request import (
    CreateUserRequest,
)
import pytest


def test_when_request_is_valid_then_no_exception_is_raised():
    request = CreateUserRequest(
        email="test@example.com",
        password="StrongPassword123!",
        username="testuser",
        name="Test User",
    )
    assert request.email == "test@example.com"
    assert request.password == "StrongPassword123!"
    assert request.username == "testuser"
    assert request.name == "Test User"


def test_when_email_is_invalid_then_exception_is_raised():
    with pytest.raises(ValueError, match="Formato de email inválido"):
        CreateUserRequest(
            email="invalid-email",
            password="StrongPassword123!",
            username="testuser",
            name="Test User",
        )


def test_when_email_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email es requerido"):
        CreateUserRequest(
            email="",
            password="StrongPassword123!",
            username="testuser",
            name="Test User",
        )


def test_when_email_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email debe tener al menos 5 caracteres"):
        CreateUserRequest(
            email="a@b",
            password="StrongPassword123!",
            username="testuser",
            name="Test User",
        )


def test_when_email_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email no debe exceder 255 caracteres"):
        CreateUserRequest(
            email="a" * 256 + "@example.com",
            password="StrongPassword123!",
            username="testuser",
            name="Test User",
        )


def test_when_username_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Nombre de usuario es requerido"):
        CreateUserRequest(
            email="test@example.com",
            password="StrongPassword123!",
            username="",
            name="Test User",
        )


def test_when_username_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Nombre de usuario debe tener al menos 3 caracteres"
    ):
        CreateUserRequest(
            email="test@example.com",
            password="StrongPassword123!",
            username="ab",
            name="Test User",
        )


def test_when_username_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Nombre de usuario no debe exceder 20 caracteres"
    ):
        CreateUserRequest(
            email="test@example.com",
            password="StrongPassword123!",
            username="a" * 21,
            name="Test User",
        )


def test_when_username_has_invalid_characters_then_exception_is_raised():
    with pytest.raises(
        ValueError,
        match="Nombre de usuario debe ser alfanumérico y puede incluir guiones bajos",
    ):
        CreateUserRequest(
            email="test@example.com",
            password="StrongPassword123!",
            username="invalid$username",
            name="Test User",
        )


def test_when_password_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Contraseña es requerida"):
        CreateUserRequest(
            email="test@example.com", password="", username="testuser", name="Test User"
        )


def test_when_password_is_too_short_then_exception_is_raised():
    short_pass = "12345"
    with pytest.raises(ValueError, match="Contraseña debe tener al menos 6 caracteres"):
        CreateUserRequest(
            email="test@example.com",
            password=short_pass,
            username="testuser",
            name="Test User",
        )


def test_when_password_is_too_long_then_exception_is_raised():
    long_pass = "a" * 21
    with pytest.raises(ValueError, match="Contraseña no debe exceder 20 caracteres"):
        CreateUserRequest(
            email="test@example.com",
            password=long_pass,
            username="testuser",
            name="Test User",
        )


def test_when_password_has_no_digit_then_exception_is_raised():
    no_digits = "NoDigitsHere!"
    with pytest.raises(ValueError, match="Contraseña debe contener al menos un dígito"):
        CreateUserRequest(
            email="test@example.com",
            password=no_digits,
            username="testuser",
            name="Test User",
        )


def test_when_password_has_no_letter_then_exception_is_raised():
    no_letters = "123456!"
    with pytest.raises(ValueError, match="Contraseña debe contener al menos una letra"):
        CreateUserRequest(
            email="test@example.com",
            password=no_letters,
            username="testuser",
            name="Test User",
        )


def test_when_password_has_no_special_char_then_exception_is_raised():
    no_special_char = "Password123"
    with pytest.raises(
        ValueError, match="Contraseña debe contener al menos un carácter especial"
    ):
        CreateUserRequest(
            email="test@example.com",
            password=no_special_char,
            username="testuser",
            name="Test User",
        )
