from unittest.mock import AsyncMock

import pytest

from src.features.assessments.save_review_question.save_review_question_request import (
    SaveReviewQuestionRequest,
)

from itmentorsoft_persistence.dto import QuestionReview
from src.features.assessments.shared.review_question_service import (
    ReviewQuestionService,
)

VALID_QUESTION_ID = "q-001-uuid-abcdef"
VALID_REVIEWER_ID = "user-001-uuid-abcdef"
VALID_REVIEW_COMMENTS = "This is a valid review comment with enough length."
VALID_STATUS = "published"


def make_valid_request() -> SaveReviewQuestionRequest:
    return SaveReviewQuestionRequest(
        question_id=VALID_QUESTION_ID,
        reviewer_id=VALID_REVIEWER_ID,
        review_comments=VALID_REVIEW_COMMENTS,
        status=VALID_STATUS,
    )


@pytest.mark.asyncio
async def test_when_user_and_question_exist_then_should_save_review_and_return_success():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    response = await service.review_question(request)

    assert response.is_success is True
    assert response.message == "Review comments saved successfully."


@pytest.mark.asyncio
async def test_when_user_and_question_exist_then_should_call_save_review():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    await service.review_question(request)

    question_repository.save_review.assert_called_once()


@pytest.mark.asyncio
async def test_when_user_and_question_exist_then_should_call_update_status():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    await service.review_question(request)

    question_repository.update_status.assert_called_once_with(
        question_id=VALID_QUESTION_ID, status=VALID_STATUS
    )


@pytest.mark.asyncio
async def test_when_reviewer_does_not_exist_then_should_return_failure():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=None)

    question_repository = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    response = await service.review_question(request)

    assert response.is_success is False
    assert f"Reviewer with ID {VALID_REVIEWER_ID} does not exist." in response.message
    question_repository.get_question.assert_not_called()
    question_repository.save_review.assert_not_called()
    question_repository.update_status.assert_not_called()


@pytest.mark.asyncio
async def test_when_question_does_not_exist_then_should_return_failure():
    user = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=None)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    response = await service.review_question(request)

    assert response.is_success is False
    assert f"Question with ID {VALID_QUESTION_ID} does not exist." in response.message
    question_repository.save_review.assert_not_called()
    question_repository.update_status.assert_not_called()


@pytest.mark.asyncio
async def test_when_user_exists_then_should_call_get_user_by_id():
    user = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=AsyncMock())
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    await service.review_question(request)

    user_repository.get_user_by_id.assert_called_once_with(VALID_REVIEWER_ID)


@pytest.mark.asyncio
async def test_when_question_exists_then_should_call_get_question():
    user = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=AsyncMock())
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    await service.review_question(request)

    question_repository.get_question.assert_called_once_with(VALID_QUESTION_ID)


@pytest.mark.asyncio
async def test_when_review_is_saved_then_should_create_question_review_with_correct_data():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    await service.review_question(request)

    call_args = question_repository.save_review.call_args
    review: QuestionReview = call_args.kwargs["review"]
    assert review.question_id == VALID_QUESTION_ID
    assert review.reviewer_id == VALID_REVIEWER_ID
    assert review.review_comments == VALID_REVIEW_COMMENTS
    assert review.review_id is not None
    assert len(review.review_id) == 32  # uuid4().hex is 32 chars


@pytest.mark.asyncio
async def test_when_update_status_is_called_then_should_use_request_status():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    await service.review_question(request)

    question_repository.update_status.assert_called_once_with(
        question_id=VALID_QUESTION_ID, status="published"
    )


@pytest.mark.asyncio
async def test_when_update_status_is_called_with_draft_then_should_use_draft_status():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = SaveReviewQuestionRequest(
        question_id=VALID_QUESTION_ID,
        reviewer_id=VALID_REVIEWER_ID,
        review_comments=VALID_REVIEW_COMMENTS,
        status="draft",
    )

    await service.review_question(request)

    question_repository.update_status.assert_called_once_with(
        question_id=VALID_QUESTION_ID, status="draft"
    )


@pytest.mark.asyncio
async def test_when_user_repository_raises_exception_then_should_propagate():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(
        side_effect=Exception("DB connection error")
    )

    question_repository = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    with pytest.raises(Exception, match="DB connection error"):
        await service.review_question(request)


@pytest.mark.asyncio
async def test_when_question_repository_raises_exception_then_should_propagate():
    user = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(side_effect=Exception("Query error"))
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    with pytest.raises(Exception, match="Query error"):
        await service.review_question(request)


@pytest.mark.asyncio
async def test_when_save_review_raises_exception_then_should_propagate():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock(side_effect=Exception("Save failed"))
    question_repository.update_status = AsyncMock()

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    with pytest.raises(Exception, match="Save failed"):
        await service.review_question(request)


@pytest.mark.asyncio
async def test_when_update_status_raises_exception_then_should_propagate():
    user = AsyncMock()
    question = AsyncMock()

    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=user)

    question_repository = AsyncMock()
    question_repository.get_question = AsyncMock(return_value=question)
    question_repository.save_review = AsyncMock()
    question_repository.update_status = AsyncMock(
        side_effect=Exception("Update failed")
    )

    service = ReviewQuestionService(user_repository, question_repository)
    request = make_valid_request()

    with pytest.raises(Exception, match="Update failed"):
        await service.review_question(request)
