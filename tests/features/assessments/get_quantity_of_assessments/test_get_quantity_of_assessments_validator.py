import pytest

from src.features.assessments.get_quantity_of_assessments.get_quantity_of_assessments_request import (
    GetQuantityOfAssessmentsRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = GetQuantityOfAssessmentsRequest(student_id="student_12345")
    assert request.student_id == "student_12345"


def test_when_student_id_is_missing_should_raise_exception():
    with pytest.raises(ValueError, match="student_id must not be empty"):
        GetQuantityOfAssessmentsRequest(student_id="")


def test_when_student_id_is_too_short_should_raise_exception():
    with pytest.raises(
        ValueError, match="student_id must be at least 5 characters long"
    ):
        GetQuantityOfAssessmentsRequest(student_id="abc")


def test_when_student_id_is_too_long_should_raise_exception():
    long_id = "a" * 101
    with pytest.raises(ValueError, match="student_id must not exceed 100 characters"):
        GetQuantityOfAssessmentsRequest(student_id=long_id)


def test_when_student_id_is_exactly_minimum_length_should_not_raise_exception():
    request = GetQuantityOfAssessmentsRequest(student_id="abcde")
    assert request.student_id == "abcde"


def test_when_student_id_is_exactly_maximum_length_should_not_raise_exception():
    max_id = "a" * 100
    request = GetQuantityOfAssessmentsRequest(student_id=max_id)
    assert request.student_id == max_id


def test_when_student_id_contains_special_characters_should_not_raise_exception():
    request = GetQuantityOfAssessmentsRequest(student_id="stu-dent_123!@#")
    assert request.student_id == "stu-dent_123!@#"


def test_when_student_id_is_numeric_string_should_not_raise_exception():
    request = GetQuantityOfAssessmentsRequest(student_id="12345")
    assert request.student_id == "12345"
