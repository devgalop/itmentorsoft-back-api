import pytest

from src.features.content_management.get_recommended_content.get_recommended_content_request import (
    GetRecommendedContentRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="student_123")
    assert request.student_id == "student_123"


def test_when_student_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="student_id must not be empty"):
        GetRecommendedContentRequest(student_id="")


def test_when_student_id_is_too_short_should_raise_exception():
    with pytest.raises(
        ValueError, match="student_id must be at least 5 characters long"
    ):
        GetRecommendedContentRequest(student_id="abc")


def test_when_student_id_is_too_long_should_raise_exception():
    with pytest.raises(ValueError, match="student_id must not exceed 100 characters"):
        GetRecommendedContentRequest(student_id="a" * 101)


def test_when_student_id_is_at_minimum_length_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="a" * 5)
    assert request.student_id == "a" * 5


def test_when_student_id_is_at_maximum_length_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="a" * 100)
    assert request.student_id == "a" * 100
