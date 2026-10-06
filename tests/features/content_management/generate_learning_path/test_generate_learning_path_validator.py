import pytest

from src.features.content_management.generate_learning_path.generate_learning_path_request import (
    GenerateLearningPathRequest,
)


def test_when_student_id_is_valid_should_not_raise():
    request = GenerateLearningPathRequest(student_id="student_123")
    assert request.student_id == "student_123"


def test_when_student_id_is_empty_should_raise():
    with pytest.raises(ValueError, match="student_id no debe estar vacío"):
        GenerateLearningPathRequest(student_id="")


def test_when_student_id_is_too_short_should_raise():
    with pytest.raises(ValueError, match="student_id debe tener al menos 5 caracteres"):
        GenerateLearningPathRequest(student_id="abc")


def test_when_student_id_is_exactly_5_characters_should_not_raise():
    request = GenerateLearningPathRequest(student_id="abcde")
    assert request.student_id == "abcde"


def test_when_student_id_is_at_maximum_length_should_not_raise():
    max_student_id = "a" * 100
    request = GenerateLearningPathRequest(student_id=max_student_id)
    assert request.student_id == max_student_id


def test_when_student_id_exceeds_100_characters_should_raise():
    long_student_id = "a" * 101
    with pytest.raises(ValueError, match="student_id no debe exceder 100 caracteres"):
        GenerateLearningPathRequest(student_id=long_student_id)
