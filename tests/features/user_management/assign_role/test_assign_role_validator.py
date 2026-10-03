from src.features.user_management.assign_role.assign_role_request import (
    AssignRoleRequest,
)
import pytest


def test_when_request_model_is_valid_then_no_validation_errors():
    request = AssignRoleRequest(user_id="12345", role="admin")
    assert request.user_id == "12345"  # nosec
    assert request.role == "admin"  # nosec


def test_when_user_id_is_missing_then_validation_error():
    with pytest.raises(ValueError, match="ID de usuario no debe estar vacío"):
        AssignRoleRequest(user_id="", role="admin")


def test_when_user_id_is_too_short_then_validation_error():
    with pytest.raises(ValueError, match="User ID must be at least 3 characters long"):
        AssignRoleRequest(user_id="1", role="admin")


def test_when_user_id_is_too_long_then_validation_error():
    with pytest.raises(
        ValueError, match="ID de usuario no debe exceder 100 caracteres"
    ):
        AssignRoleRequest(user_id="1" * 101, role="admin")


def test_when_role_is_missing_then_validation_error():
    with pytest.raises(ValueError, match="Rol no debe estar vacío"):
        AssignRoleRequest(user_id="1", role="")


def test_when_role_is_too_short_then_validation_error():
    with pytest.raises(ValueError, match="Rol debe tener al menos 3 caracteres"):
        AssignRoleRequest(user_id="1", role="a")


def test_when_role_is_too_long_then_validation_error():
    with pytest.raises(
        ValueError, match="Role must be no more than 50 characters long"
    ):
        AssignRoleRequest(user_id="1", role="a" * 51)
