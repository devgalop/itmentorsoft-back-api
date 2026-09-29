import pytest

from src.features.assessments.get_all_question_versions.get_all_question_versions_request import (
    GetAllQuestionVersionsRequest,
)


def test_valid_question_id():
    request = GetAllQuestionVersionsRequest(question_id="question-123")
    assert request.question_id == "question-123"


def test_valid_question_id_min_length():
    request = GetAllQuestionVersionsRequest(question_id="abc")
    assert request.question_id == "abc"


def test_valid_question_id_max_length():
    question_id = "q" * 100
    request = GetAllQuestionVersionsRequest(question_id=question_id)
    assert request.question_id == question_id


def test_empty_question_id_raises_error():
    with pytest.raises(ValueError, match="question_id must not be empty"):
        GetAllQuestionVersionsRequest(question_id="")


def test_question_id_too_short_raises_error():
    with pytest.raises(
        ValueError, match="question_id must be at least 3 characters long"
    ):
        GetAllQuestionVersionsRequest(question_id="ab")


def test_question_id_too_long_raises_error():
    question_id = "q" * 101
    with pytest.raises(
        ValueError, match="question_id must be at most 100 characters long"
    ):
        GetAllQuestionVersionsRequest(question_id=question_id)
