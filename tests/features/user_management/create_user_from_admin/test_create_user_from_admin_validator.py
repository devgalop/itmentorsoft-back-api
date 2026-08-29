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
    with pytest.raises(ValueError, match="Invalid email format"):
        CreateUserFromAdminRequest(
            email="invalid-email", username="testuser", role="student", name="Test User"
        )


def test_when_email_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email is required"):
        CreateUserFromAdminRequest(
            email="", username="testuser", role="student", name="Test User"
        )


def test_when_email_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Email must be at least 5 characters long"):
        CreateUserFromAdminRequest(
            email="a@b", username="testuser", role="student", name="Test User"
        )


def test_when_email_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Email must be no more than 255 characters long"
    ):
        CreateUserFromAdminRequest(
            email="a" * 256 + "@example.com",
            username="testuser",
            role="student",
            name="Test User",
        )


def test_when_username_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Username is required"):
        CreateUserFromAdminRequest(
            email="test@example.com", username="", role="student", name="Test User"
        )


def test_when_username_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Username must be at least 3 characters long"):
        CreateUserFromAdminRequest(
            email="test@example.com", username="ab", role="student", name="Test User"
        )


def test_when_username_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Username must be no more than 20 characters long"
    ):
        CreateUserFromAdminRequest(
            email="test@example.com",
            username="a" * 21,
            role="student",
            name="Test User",
        )


def test_when_username_has_invalid_characters_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Username must be alphanumeric and can include underscores"
    ):
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
    with pytest.raises(ValueError, match="Role must be at least 3 characters long"):
        CreateUserFromAdminRequest(
            email="test@example.com", username="testuser", role="ab", name="Test User"
        )


def test_when_role_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Role must be no more than 20 characters long"
    ):
        CreateUserFromAdminRequest(
            email="test@example.com",
            username="testuser",
            role="a" * 21,
            name="Test User",
        )
