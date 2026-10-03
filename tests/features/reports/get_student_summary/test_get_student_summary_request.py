from src.features.reports.get_student_summary.get_student_summary_request import (
    GetStudentSummaryRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetStudentSummaryRequest(student_id="abc123")
    assert request.student_id == "abc123"


def test_when_student_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="student_id no debe estar vacío"):
        GetStudentSummaryRequest(student_id="")


def test_when_student_id_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="student_id debe tener al menos 5 caracteres"):
        GetStudentSummaryRequest(student_id="abc")


def test_when_student_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="student_id no debe exceder 100 caracteres"):
        GetStudentSummaryRequest(student_id="a" * 101)


def test_when_student_id_is_exactly_5_characters_then_valid():
    request = GetStudentSummaryRequest(student_id="abcde")
    assert request.student_id == "abcde"


def test_when_student_id_is_exactly_100_characters_then_valid():
    request = GetStudentSummaryRequest(student_id="a" * 100)
    assert request.student_id == "a" * 100
