import pytest

from src.features.assessments.save_assessments_answers.save_assessments_answers_request import (
    AssessmentAnswer,
    SaveAssessmentsAnswersRequest,
)

VALID_QUESTION_ID = "q-001-uuid-abc"
VALID_ANSWER = "This is a valid answer text."
VALID_ASSESSMENT_ID = "assess-001-uuid-abc"
VALID_USER_ID = "user-001-uuid-abcdef"


def make_valid_answer(
    question_id: str = VALID_QUESTION_ID,
    answer: str = VALID_ANSWER,
    takes_time_seconds: int = 60,
) -> AssessmentAnswer:
    return AssessmentAnswer(
        question_id=question_id, answer=answer, takes_time_seconds=takes_time_seconds
    )


def make_valid_request(
    assessment_id: str = VALID_ASSESSMENT_ID,
    user_id: str = VALID_USER_ID,
    answers: list | None = None,
) -> SaveAssessmentsAnswersRequest:
    return SaveAssessmentsAnswersRequest(
        assessment_id=assessment_id,
        user_id=user_id,
        answers=answers or [make_valid_answer()],
    )


# --- AssessmentAnswer validator tests ---


def test_when_answer_is_valid_then_no_exception_is_raised():
    answer = make_valid_answer()
    assert answer.question_id == VALID_QUESTION_ID
    assert answer.answer == VALID_ANSWER
    assert answer.takes_time_seconds == 60


def test_when_question_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="question_id must not be empty"):
        AssessmentAnswer(question_id="", answer=VALID_ANSWER, takes_time_seconds=60)


def test_when_question_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="question_id debe tener al menos 5 caracteres"
    ):
        AssessmentAnswer(question_id="abc", answer=VALID_ANSWER, takes_time_seconds=60)


def test_when_question_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="question_id must not exceed 200 characters"):
        AssessmentAnswer(
            question_id="q" * 201, answer=VALID_ANSWER, takes_time_seconds=60
        )


def test_when_answer_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="answer must not be empty"):
        AssessmentAnswer(
            question_id=VALID_QUESTION_ID, answer="", takes_time_seconds=60
        )


def test_when_answer_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="answer must not exceed 600 characters"):
        AssessmentAnswer(
            question_id=VALID_QUESTION_ID, answer="a" * 601, takes_time_seconds=60
        )


def test_when_takes_time_seconds_is_negative_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="takes_time_seconds must be a non-negative integer"
    ):
        AssessmentAnswer(
            question_id=VALID_QUESTION_ID, answer=VALID_ANSWER, takes_time_seconds=-1
        )


def test_when_takes_time_seconds_is_zero_then_no_exception_is_raised():
    answer = AssessmentAnswer(
        question_id=VALID_QUESTION_ID, answer=VALID_ANSWER, takes_time_seconds=0
    )
    assert answer.takes_time_seconds == 0


# --- SaveAssessmentsAnswersRequest validator tests ---


def test_when_request_is_valid_then_no_exception_is_raised():
    request = make_valid_request()
    assert request.assessment_id == VALID_ASSESSMENT_ID
    assert request.user_id == VALID_USER_ID
    assert len(request.answers) == 1


def test_when_assessment_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="assessment_id must not be empty"):
        SaveAssessmentsAnswersRequest(
            assessment_id="", user_id=VALID_USER_ID, answers=[make_valid_answer()]
        )


def test_when_assessment_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="assessment_id must be at least 5 characters long"
    ):
        SaveAssessmentsAnswersRequest(
            assessment_id="abc", user_id=VALID_USER_ID, answers=[make_valid_answer()]
        )


def test_when_assessment_id_is_too_long_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="assessment_id must not exceed 200 characters"
    ):
        SaveAssessmentsAnswersRequest(
            assessment_id="a" * 201,
            user_id=VALID_USER_ID,
            answers=[make_valid_answer()],
        )


def test_when_user_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="user_id must not be empty"):
        SaveAssessmentsAnswersRequest(
            assessment_id=VALID_ASSESSMENT_ID, user_id="", answers=[make_valid_answer()]
        )


def test_when_user_id_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="user_id must be at least 5 characters long"):
        SaveAssessmentsAnswersRequest(
            assessment_id=VALID_ASSESSMENT_ID,
            user_id="abc",
            answers=[make_valid_answer()],
        )


def test_when_user_id_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="user_id must not exceed 200 characters"):
        SaveAssessmentsAnswersRequest(
            assessment_id=VALID_ASSESSMENT_ID,
            user_id="u" * 201,
            answers=[make_valid_answer()],
        )
