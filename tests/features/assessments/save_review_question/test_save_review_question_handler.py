from unittest.mock import AsyncMock

import pytest

from src.features.assessments.save_review_question.save_review_question_handler import (
    SaveReviewQuestionHandler,
)
from src.features.assessments.save_review_question.save_review_question_request import (
    SaveReviewQuestionRequest,
)
from src.features.assessments.save_review_question.save_review_question_response import (
    SaveReviewQuestionResponse,
)

VALID_QUESTION_ID = "q-001-uuid-abcdef"
VALID_REVIEWER_ID = "user-001-uuid-abcdef"
VALID_REVIEW_COMMENTS = "This is a valid review comment with enough length."
VALID_STATUS = "published"


def make_valid_request(status: str = VALID_STATUS) -> SaveReviewQuestionRequest:
    return SaveReviewQuestionRequest(
        question_id=VALID_QUESTION_ID,
        reviewer_id=VALID_REVIEWER_ID,
        review_comments=VALID_REVIEW_COMMENTS,
        status=status,
    )


@pytest.mark.asyncio
async def test_when_service_returns_success_then_handler_should_return_success():
    service_response = SaveReviewQuestionResponse(
        is_success=True, message="Review comments saved successfully."
    )

    service = AsyncMock()
    service.review_question = AsyncMock(return_value=service_response)

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request()

    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Review comments saved successfully."


@pytest.mark.asyncio
async def test_when_service_returns_failure_then_handler_should_return_same_failure():
    service_response = SaveReviewQuestionResponse(
        is_success=False, message="Question with ID q-001 does not exist."
    )

    service = AsyncMock()
    service.review_question = AsyncMock(return_value=service_response)

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request()

    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Question with ID q-001 does not exist."


@pytest.mark.asyncio
async def test_when_handler_is_called_then_should_delegate_to_service():
    service_response = SaveReviewQuestionResponse(is_success=True, message="OK")

    service = AsyncMock()
    service.review_question = AsyncMock(return_value=service_response)

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request()

    await handler.handle(request)

    service.review_question.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_handler_is_called_then_should_return_same_response_as_service():
    service_response = SaveReviewQuestionResponse(
        is_success=True, message="Custom message"
    )

    service = AsyncMock()
    service.review_question = AsyncMock(return_value=service_response)

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request()

    response = await handler.handle(request)

    assert response is service_response


@pytest.mark.asyncio
async def test_when_status_is_invalid_then_should_return_failure():
    service = AsyncMock()

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request(status="nonexistent_status")

    response = await handler.handle(request)

    assert response.is_success is False
    assert "Estado inválido 'nonexistent_status'" in response.message
    assert "draft" in response.message
    assert "published" in response.message
    assert "archived" in response.message
    service.review_question.assert_not_called()


@pytest.mark.asyncio
async def test_when_status_is_draft_then_should_delegate_to_service():
    service_response = SaveReviewQuestionResponse(
        is_success=True, message="Review comments saved successfully."
    )

    service = AsyncMock()
    service.review_question = AsyncMock(return_value=service_response)

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request(status="draft")

    response = await handler.handle(request)

    assert response.is_success is True
    service.review_question.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_status_is_published_then_should_delegate_to_service():
    service_response = SaveReviewQuestionResponse(
        is_success=True, message="Review comments saved successfully."
    )

    service = AsyncMock()
    service.review_question = AsyncMock(return_value=service_response)

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request(status="published")

    response = await handler.handle(request)

    assert response.is_success is True
    service.review_question.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_status_is_archived_then_should_delegate_to_service():
    service_response = SaveReviewQuestionResponse(
        is_success=True, message="Review comments saved successfully."
    )

    service = AsyncMock()
    service.review_question = AsyncMock(return_value=service_response)

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request(status="archived")

    response = await handler.handle(request)

    assert response.is_success is True
    service.review_question.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_status_is_not_in_enum_then_should_return_failure():
    service = AsyncMock()

    handler = SaveReviewQuestionHandler(service)
    # Use a non-empty string that passes Pydantic validation but is not a valid QuestionStatus
    request = SaveReviewQuestionRequest(
        question_id=VALID_QUESTION_ID,
        reviewer_id=VALID_REVIEWER_ID,
        review_comments=VALID_REVIEW_COMMENTS,
        status="invalid_status_value",
    )

    response = await handler.handle(request)

    assert response.is_success is False
    assert "Estado inválido 'invalid_status_value'" in response.message
    assert "draft" in response.message
    assert "published" in response.message
    assert "archived" in response.message
    service.review_question.assert_not_called()


@pytest.mark.asyncio
async def test_when_service_raises_exception_then_should_propagate():
    service = AsyncMock()
    service.review_question = AsyncMock(side_effect=Exception("Database error"))

    handler = SaveReviewQuestionHandler(service)
    request = make_valid_request()

    with pytest.raises(Exception, match="Database error"):
        await handler.handle(request)
