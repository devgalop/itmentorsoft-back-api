import pytest

from src.features.assessments.update_question_status.update_question_status_request import (
    UpdateQuestionStatusRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = UpdateQuestionStatusRequest(question_id="question_12345", status=True)
    assert request.question_id == "question_12345"
    assert request.status is True


def test_when_question_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="question_id no debe estar vacío"):
        UpdateQuestionStatusRequest(question_id="", status=True)


def test_when_question_id_is_too_short_should_raise_exception():
    with pytest.raises(
        ValueError, match="question_id debe tener al menos 5 caracteres"
    ):
        UpdateQuestionStatusRequest(question_id="q12", status=True)


def test_when_question_id_is_too_long_should_raise_exception():
    long_id = "q" * 101
    with pytest.raises(ValueError, match="question_id no debe exceder 100 caracteres"):
        UpdateQuestionStatusRequest(question_id=long_id, status=True)


def test_when_question_id_is_exactly_5_characters_should_not_raise():
    request = UpdateQuestionStatusRequest(question_id="ques1", status=True)
    assert request.question_id == "ques1"


def test_when_question_id_is_exactly_100_characters_should_not_raise():
    valid_id = "q" * 100
    request = UpdateQuestionStatusRequest(question_id=valid_id, status=True)
    assert request.question_id == valid_id


def test_when_status_is_true_should_accept():
    request = UpdateQuestionStatusRequest(question_id="question_12345", status=True)
    assert request.status is True


def test_when_status_is_false_should_accept():
    request = UpdateQuestionStatusRequest(question_id="question_12345", status=False)
    assert request.status is False
