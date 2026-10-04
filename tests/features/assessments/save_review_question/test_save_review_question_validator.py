import pytest

from src.features.assessments.save_review_question.save_review_question_request import (
    SaveReviewQuestionRequest,
)

VALID_QUESTION_ID = "q-001-uuid-abcdef"
VALID_REVIEWER_ID = "user-001-uuid-abcdef"
VALID_REVIEW_COMMENTS = "This is a valid review comment text."
VALID_STATUS = "published"


def make_valid_request(
    question_id: str = VALID_QUESTION_ID,
    reviewer_id: str = VALID_REVIEWER_ID,
    review_comments: str = VALID_REVIEW_COMMENTS,
    status: str = VALID_STATUS,
) -> SaveReviewQuestionRequest:
    return SaveReviewQuestionRequest(
        question_id=question_id,
        reviewer_id=reviewer_id,
        review_comments=review_comments,
        status=status,
    )


# --- question_id validator tests ---


def test_when_question_id_is_valid_then_no_exception_is_raised():
    request = make_valid_request()
    assert request.question_id == VALID_QUESTION_ID


def test_when_question_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="question_id no debe estar vacío"):
        make_valid_request(question_id="")


def test_when_question_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="question_id debe tener al menos 5 caracteres"
    ):
        make_valid_request(question_id="abc")


def test_when_question_id_is_at_minimum_boundary_then_no_exception_is_raised():
    request = make_valid_request(question_id="abcde")
    assert request.question_id == "abcde"


def test_when_question_id_is_at_maximum_boundary_then_no_exception_is_raised():
    request = make_valid_request(question_id="q" * 100)
    assert request.question_id == "q" * 100


def test_when_question_id_exceeds_maximum_then_exception_is_raised():
    with pytest.raises(ValueError, match="question_id no debe exceder 100 caracteres"):
        make_valid_request(question_id="q" * 101)


# --- reviewer_id validator tests ---


def test_when_reviewer_id_is_valid_then_no_exception_is_raised():
    request = make_valid_request()
    assert request.reviewer_id == VALID_REVIEWER_ID


def test_when_reviewer_id_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="reviewer_id no debe estar vacío"):
        make_valid_request(reviewer_id="")


def test_when_reviewer_id_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="reviewer_id debe tener al menos 5 caracteres"
    ):
        make_valid_request(reviewer_id="abc")


def test_when_reviewer_id_is_at_minimum_boundary_then_no_exception_is_raised():
    request = make_valid_request(reviewer_id="abcde")
    assert request.reviewer_id == "abcde"


def test_when_reviewer_id_is_at_maximum_boundary_then_no_exception_is_raised():
    request = make_valid_request(reviewer_id="u" * 100)
    assert request.reviewer_id == "u" * 100


def test_when_reviewer_id_exceeds_maximum_then_exception_is_raised():
    with pytest.raises(ValueError, match="reviewer_id no debe exceder 100 caracteres"):
        make_valid_request(reviewer_id="u" * 101)


# --- review_comments validator tests ---


def test_when_review_comments_is_valid_then_no_exception_is_raised():
    request = make_valid_request()
    assert request.review_comments == VALID_REVIEW_COMMENTS


def test_when_review_comments_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="review_comments no debe estar vacío"):
        make_valid_request(review_comments="")


def test_when_review_comments_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="review_comments debe tener al menos 10 caracteres"
    ):
        make_valid_request(review_comments="short")


def test_when_review_comments_is_at_minimum_boundary_then_no_exception_is_raised():
    request = make_valid_request(review_comments="1234567890")
    assert request.review_comments == "1234567890"


def test_when_review_comments_is_at_maximum_boundary_then_no_exception_is_raised():
    request = make_valid_request(review_comments="c" * 1000)
    assert request.review_comments == "c" * 1000


def test_when_review_comments_exceeds_maximum_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="review_comments no debe exceder 1000 caracteres"
    ):
        make_valid_request(review_comments="c" * 1001)


# --- status validator tests ---


def test_when_status_is_valid_then_no_exception_is_raised():
    request = make_valid_request()
    assert request.status == VALID_STATUS


def test_when_status_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="status no debe estar vacío"):
        make_valid_request(status="")


def test_when_status_is_draft_then_no_exception_is_raised():
    request = make_valid_request(status="draft")
    assert request.status == "draft"


def test_when_status_is_published_then_no_exception_is_raised():
    request = make_valid_request(status="published")
    assert request.status == "published"


def test_when_status_is_archived_then_no_exception_is_raised():
    request = make_valid_request(status="archived")
    assert request.status == "archived"


def test_when_status_is_custom_value_then_no_exception_is_raised():
    request = make_valid_request(status="custom_status")
    assert request.status == "custom_status"


# --- full request validation tests ---


def test_when_all_fields_are_valid_then_request_is_created_successfully():
    request = make_valid_request()
    assert request.question_id == VALID_QUESTION_ID
    assert request.reviewer_id == VALID_REVIEWER_ID
    assert request.review_comments == VALID_REVIEW_COMMENTS
    assert request.status == VALID_STATUS


def test_when_multiple_fields_are_invalid_then_first_validation_error_is_raised():
    with pytest.raises(ValueError):
        SaveReviewQuestionRequest(
            question_id="",
            reviewer_id="",
            review_comments="",
            status="",
        )
