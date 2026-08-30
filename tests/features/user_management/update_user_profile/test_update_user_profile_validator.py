import pytest

from src.features.user_management.update_user_profile.update_user_profile_request import (
    UpdateUserProfileRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = UpdateUserProfileRequest(
        user_id="user_id", username="valid_username", name="Valid Name"
    )
    assert request.user_id == "user_id"
    assert request.username == "valid_username"
    assert request.name == "Valid Name"


def test_when_user_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="User ID is required"):
        UpdateUserProfileRequest(
            user_id="", username="valid_username", name="Valid Name"
        )


def test_when_user_id_is_too_long_should_raise_exception():
    with pytest.raises(
        ValueError, match="User ID must be no more than 100 characters long"
    ):
        UpdateUserProfileRequest(
            user_id="a" * 101, username="valid_username", name="Valid Name"
        )


def test_when_username_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="Username is required"):
        UpdateUserProfileRequest(user_id="user_id", username="", name="Valid Name")


def test_when_username_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="Username must be at least 3 characters long"):
        UpdateUserProfileRequest(user_id="user_id", username="ab", name="Valid Name")


def test_when_username_is_too_long_should_raise_exception():
    with pytest.raises(
        ValueError, match="Username must be no more than 20 characters long"
    ):
        UpdateUserProfileRequest(
            user_id="user_id", username="a" * 21, name="Valid Name"
        )


def test_when_username_has_special_characters_should_raise_exception():
    with pytest.raises(
        ValueError,
        match="Username must be alphanumeric and can include underscores",
    ):
        UpdateUserProfileRequest(
            user_id="user_id", username="user@name!", name="Valid Name"
        )


def test_when_username_has_spaces_should_raise_exception():
    with pytest.raises(
        ValueError,
        match="Username must be alphanumeric and can include underscores",
    ):
        UpdateUserProfileRequest(
            user_id="user_id", username="user name", name="Valid Name"
        )


def test_when_username_contains_underscores_should_not_raise_exception():
    request = UpdateUserProfileRequest(
        user_id="user_id", username="valid_user_name", name="Valid Name"
    )
    assert request.username == "valid_user_name"
    assert request.name == "Valid Name"
