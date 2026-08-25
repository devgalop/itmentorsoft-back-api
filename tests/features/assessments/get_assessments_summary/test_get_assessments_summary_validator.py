import pytest

from src.features.assessments.get_assessments_summary.get_assessments_summary_request import (
    GetAssessmentsSummaryRequest,
)

# ---------------------------------------------------------------------------
# Valid requests
# ---------------------------------------------------------------------------


def test_when_request_is_valid_should_not_raise_exception():
    request = GetAssessmentsSummaryRequest(
        student_id="student_12345", page=1, page_size=20
    )
    assert request.student_id == "student_12345"
    assert request.page == 1
    assert request.page_size == 20


def test_when_request_uses_defaults_should_apply_default_values():
    request = GetAssessmentsSummaryRequest(student_id="student_12345")
    assert request.student_id == "student_12345"
    assert request.page == 0
    assert request.page_size == 10


# ---------------------------------------------------------------------------
# student_id validation
# ---------------------------------------------------------------------------


def test_when_student_id_is_empty_should_raise_value_error():
    with pytest.raises(ValueError, match="Student ID must not be empty."):
        GetAssessmentsSummaryRequest(student_id="")


def test_when_student_id_is_too_short_should_raise_value_error():
    with pytest.raises(
        ValueError, match="Student ID must be at least 5 characters long."
    ):
        GetAssessmentsSummaryRequest(student_id="abc")


def test_when_student_id_is_exactly_minimum_length_should_not_raise_exception():
    request = GetAssessmentsSummaryRequest(student_id="abcde")
    assert request.student_id == "abcde"


def test_when_student_id_is_exactly_maximum_length_should_not_raise_exception():
    request = GetAssessmentsSummaryRequest(student_id="a" * 100)
    assert request.student_id == "a" * 100


def test_when_student_id_exceeds_maximum_length_should_raise_value_error():
    with pytest.raises(
        ValueError, match="Student ID must be at most 100 characters long."
    ):
        GetAssessmentsSummaryRequest(student_id="a" * 101)


# ---------------------------------------------------------------------------
# page validation
# ---------------------------------------------------------------------------


def test_when_page_is_negative_should_raise_value_error():
    with pytest.raises(ValueError, match="Value must be a non-negative integer."):
        GetAssessmentsSummaryRequest(student_id="student_12345", page=-1)


def test_when_page_is_zero_should_not_raise_exception():
    request = GetAssessmentsSummaryRequest(student_id="student_12345", page=0)
    assert request.page == 0


def test_when_page_is_positive_should_not_raise_exception():
    request = GetAssessmentsSummaryRequest(student_id="student_12345", page=10)
    assert request.page == 10


# ---------------------------------------------------------------------------
# page_size validation
# ---------------------------------------------------------------------------


def test_when_page_size_is_negative_should_raise_value_error():
    with pytest.raises(ValueError, match="Value must be a non-negative integer."):
        GetAssessmentsSummaryRequest(student_id="student_12345", page_size=-5)


def test_when_page_size_is_zero_should_raise_value_error():
    with pytest.raises(ValueError, match="Page size must be a positive integer."):
        GetAssessmentsSummaryRequest(student_id="student_12345", page_size=0)


def test_when_page_size_is_one_should_not_raise_exception():
    request = GetAssessmentsSummaryRequest(student_id="student_12345", page_size=1)
    assert request.page_size == 1


def test_when_page_size_is_one_hundred_should_not_raise_exception():
    request = GetAssessmentsSummaryRequest(student_id="student_12345", page_size=100)
    assert request.page_size == 100


def test_when_page_size_exceeds_maximum_should_raise_value_error():
    with pytest.raises(ValueError, match="Page size must not exceed 100."):
        GetAssessmentsSummaryRequest(student_id="student_12345", page_size=101)
