import pytest

from src.features.user_management.update_user_status.update_user_status_request import (
    UpdateUserStatusRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = UpdateUserStatusRequest(user_id="valid_user_id", new_status="active")
    assert request.user_id == "valid_user_id"
    assert request.new_status == "active"


def test_when_user_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="User ID must not be empty"):
        UpdateUserStatusRequest(user_id="", new_status="active")


def test_when_user_id_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="User ID must be at least 5 characters long"):
        UpdateUserStatusRequest(user_id="abc", new_status="active")


def test_when_user_id_is_too_long_should_raise_exception():
    with pytest.raises(
        ValueError, match="User ID must be no more than 100 characters long"
    ):
        UpdateUserStatusRequest(user_id="a" * 101, new_status="active")


def test_when_new_status_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="New status must not be empty"):
        UpdateUserStatusRequest(user_id="valid_user_id", new_status="")


def test_when_new_status_is_too_short_should_raise_exception():
    with pytest.raises(
        ValueError, match="New status must be at least 3 characters long"
    ):
        UpdateUserStatusRequest(user_id="valid_user_id", new_status="ab")


def test_when_new_status_is_too_long_should_raise_exception():
    with pytest.raises(
        ValueError, match="New status must be no more than 20 characters long"
    ):
        UpdateUserStatusRequest(user_id="valid_user_id", new_status="a" * 21)
