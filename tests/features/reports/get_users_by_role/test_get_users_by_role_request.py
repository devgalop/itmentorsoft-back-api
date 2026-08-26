import pytest

from src.features.reports.get_users_by_role.get_users_by_role_request import (
    GetUsersByRoleRequest,
)


def test_when_role_is_valid_should_not_raise_exception():
    request = GetUsersByRoleRequest(role="admin")
    assert request.role == "admin"


def test_when_role_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="Role must not be empty"):
        GetUsersByRoleRequest(role="")


def test_when_role_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="Role must be at least 3 characters long"):
        GetUsersByRoleRequest(role="ab")


def test_when_role_is_too_long_should_raise_exception():
    with pytest.raises(
        ValueError, match="Role must be no more than 20 characters long"
    ):
        GetUsersByRoleRequest(role="a" * 21)


def test_when_role_is_exactly_3_characters_should_be_valid():
    request = GetUsersByRoleRequest(role="abc")
    assert request.role == "abc"


def test_when_role_is_exactly_20_characters_should_be_valid():
    request = GetUsersByRoleRequest(role="a" * 20)
    assert request.role == "a" * 20
