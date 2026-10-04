import pytest

from src.features.user_management.update_user_status.update_user_status_request import (
    UpdateUserStatusRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = UpdateUserStatusRequest(user_id="valid_user_id", new_status="active")
    assert request.user_id == "valid_user_id"
    assert request.new_status == "active"


def test_when_user_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="ID de usuario no debe estar vacío"):
        UpdateUserStatusRequest(user_id="", new_status="active")


def test_when_user_id_is_too_short_should_raise_exception():
    with pytest.raises(
        ValueError, match="ID de usuario debe tener al menos 5 caracteres"
    ):
        UpdateUserStatusRequest(user_id="abc", new_status="active")


def test_when_user_id_is_too_long_should_raise_exception():
    with pytest.raises(
        ValueError, match="ID de usuario no debe exceder 100 caracteres"
    ):
        UpdateUserStatusRequest(user_id="a" * 101, new_status="active")


def test_when_new_status_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="status no debe estar vacío"):
        UpdateUserStatusRequest(user_id="valid_user_id", new_status="")


def test_when_new_status_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="Estado debe tener al menos 3 caracteres"):
        UpdateUserStatusRequest(user_id="valid_user_id", new_status="ab")


def test_when_new_status_is_too_long_should_raise_exception():
    with pytest.raises(ValueError, match="Estado no debe exceder 20 caracteres"):
        UpdateUserStatusRequest(user_id="valid_user_id", new_status="a" * 21)
