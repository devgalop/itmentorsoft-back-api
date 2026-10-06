import pytest

from src.features.content_management.get_recommended_content.get_recommended_content_request import (
    GetRecommendedContentRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="student_123", path_id="path_456")
    assert request.student_id == "student_123"
    assert request.path_id == "path_456"


def test_when_student_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="student_id no debe estar vacío"):
        GetRecommendedContentRequest(student_id="", path_id="path_456")


def test_when_student_id_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="student_id debe tener al menos 5 caracteres"):
        GetRecommendedContentRequest(student_id="abc", path_id="path_456")


def test_when_student_id_is_too_long_should_raise_exception():
    with pytest.raises(ValueError, match="student_id no debe exceder 100 caracteres"):
        GetRecommendedContentRequest(student_id="a" * 101, path_id="path_456")


def test_when_student_id_is_at_minimum_length_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="a" * 5, path_id="path_456")
    assert request.student_id == "a" * 5


def test_when_student_id_is_at_maximum_length_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="a" * 100, path_id="path_456")
    assert request.student_id == "a" * 100


def test_when_path_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="ID de ruta no debe estar vacío"):
        GetRecommendedContentRequest(student_id="student_123", path_id="")


def test_when_path_id_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="ID de ruta debe tener al menos 5 caracteres"):
        GetRecommendedContentRequest(student_id="student_123", path_id="abc")


def test_when_path_id_is_too_long_should_raise_exception():
    with pytest.raises(ValueError, match="ID de ruta no debe exceder 100 caracteres"):
        GetRecommendedContentRequest(student_id="student_123", path_id="a" * 101)


def test_when_path_id_is_at_minimum_length_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="student_123", path_id="a" * 5)
    assert request.path_id == "a" * 5


def test_when_path_id_is_at_maximum_length_should_not_raise_exception():
    request = GetRecommendedContentRequest(student_id="student_123", path_id="a" * 100)
    assert request.path_id == "a" * 100
