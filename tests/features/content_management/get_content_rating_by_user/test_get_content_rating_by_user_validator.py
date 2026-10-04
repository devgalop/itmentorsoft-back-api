import pytest
from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_request import (
    GetContentRatingByUserRequest,
)


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetContentRatingByUserRequest(
        user_id="valid_user_id_123", content_id="valid_content_id_456"
    )
    assert request.user_id == "valid_user_id_123"
    assert request.content_id == "valid_content_id_456"


def test_when_user_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="ID de usuario no debe estar vacío"):
        GetContentRatingByUserRequest(user_id="", content_id="valid_content_id_456")


def test_when_user_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="ID de usuario debe tener al menos 10 caracteres"
    ):
        GetContentRatingByUserRequest(
            user_id="short", content_id="valid_content_id_456"
        )


def test_when_user_id_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="ID de usuario no debe exceder 100 caracteres"
    ):
        GetContentRatingByUserRequest(
            user_id="a" * 101, content_id="valid_content_id_456"
        )


def test_when_content_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="ID de contenido no debe estar vacío"):
        GetContentRatingByUserRequest(user_id="valid_user_id_123", content_id="")


def test_when_content_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="ID de contenido debe tener al menos 10 caracteres"
    ):
        GetContentRatingByUserRequest(user_id="valid_user_id_123", content_id="short")


def test_when_content_id_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="ID de contenido no debe exceder 100 caracteres"
    ):
        GetContentRatingByUserRequest(user_id="valid_user_id_123", content_id="a" * 101)
