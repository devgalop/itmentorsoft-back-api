from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_handler import (
    GetPendingApprovalQuestionsHandler,
)
from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_request import (
    GetPendingApprovalQuestionsRequest,
)
from itmentorsoft_persistence.dto import PaginatedQuestionsResult
from itmentorsoft_persistence.dto import QuestionDetails

PAGE = 0
PAGE_SIZE = 10


def make_question_details(
    question_id: str, text: str, status: str = "draft"
) -> QuestionDetails:
    return QuestionDetails(
        question_id=question_id,
        text_to_evaluate=text,
        concept="test-concept",
        definition="test-definition",
        simple_explanation="test-explanation",
        correct_sample="test-correct",
        wrong_sample="test-wrong",
        status=status,
        difficulty="básico",
        classification="test-classification",
        version=1,
    )


@pytest.mark.asyncio
async def test_when_repository_returns_questions_then_should_return_success():
    questions = [
        make_question_details("q1", "What is OOP?"),
        make_question_details("q2", "Explain encapsulation"),
    ]

    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(
        return_value=PaginatedQuestionsResult(items=questions, total=2)
    )

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=PAGE, page_size=PAGE_SIZE)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Pending approval questions retrieved successfully."
    assert response.total == 2
    assert len(response.questions) == 2


@pytest.mark.asyncio
async def test_when_repository_returns_questions_then_should_return_question_data():
    questions = [
        make_question_details("q1", "What is OOP?"),
        make_question_details("q2", "Explain encapsulation"),
        make_question_details("q3", "Define inheritance"),
    ]

    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(
        return_value=PaginatedQuestionsResult(items=questions, total=3)
    )

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=PAGE, page_size=PAGE_SIZE)
    response = await handler.handle(request)

    assert response.questions is not None
    assert response.questions[0].question_id == "q1"
    assert response.questions[0].text_to_evaluate == "What is OOP?"
    assert response.questions[1].question_id == "q2"
    assert response.questions[2].question_id == "q3"


@pytest.mark.asyncio
async def test_when_repository_returns_empty_total_then_should_return_success_with_message():
    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(
        return_value=PaginatedQuestionsResult(items=[], total=0)
    )

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=PAGE, page_size=PAGE_SIZE)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "No pending approval questions found."
    assert response.questions == []
    assert response.total == 0


@pytest.mark.asyncio
async def test_when_repository_returns_none_then_should_return_failure():
    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(return_value=None)

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=PAGE, page_size=PAGE_SIZE)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Failed to retrieve pending approval questions."
    assert response.questions == []
    assert response.total == 0


@pytest.mark.asyncio
async def test_when_repository_returns_empty_list_then_should_return_failure():
    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(return_value=[])

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=PAGE, page_size=PAGE_SIZE)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Failed to retrieve pending approval questions."
    assert response.questions == []
    assert response.total == 0


@pytest.mark.asyncio
async def test_when_repository_raises_exception_then_should_return_failure():
    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(
        side_effect=Exception("Database connection error")
    )

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=PAGE, page_size=PAGE_SIZE)
    response = await handler.handle(request)

    assert response.is_success is False
    assert "Invalid request" in response.message
    assert "Database connection error" in response.message
    assert response.questions == []
    assert response.total == 0


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_call_repository_with_correct_params():
    questions = [make_question_details("q1", "What is OOP?")]

    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(
        return_value=PaginatedQuestionsResult(items=questions, total=1)
    )

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=2, page_size=25)
    await handler.handle(request)

    repository.get_questions_pending_review.assert_called_once_with(2, 25)


@pytest.mark.asyncio
async def test_when_repository_returns_paginated_results_then_should_return_correct_total():
    questions = [make_question_details(f"q{i}", f"Question {i}") for i in range(5)]

    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(
        return_value=PaginatedQuestionsResult(items=questions, total=47)
    )

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=1, page_size=5)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.total == 47
    assert len(response.questions) == 5


@pytest.mark.asyncio
async def test_when_repository_returns_questions_then_response_items_match_repository_items():
    questions = [
        make_question_details("q-abc", "What is a class?"),
        make_question_details("q-def", "What is an object?"),
    ]

    repository = AsyncMock()
    repository.get_questions_pending_review = AsyncMock(
        return_value=PaginatedQuestionsResult(items=questions, total=2)
    )

    handler = GetPendingApprovalQuestionsHandler(repository)

    request = GetPendingApprovalQuestionsRequest(page=PAGE, page_size=PAGE_SIZE)
    response = await handler.handle(request)

    assert len(response.questions) == 2
    assert isinstance(response.questions[0], QuestionDetails)
    assert response.questions[0].question_id == "q-abc"
    assert response.questions[0].text_to_evaluate == "What is a class?"
    assert response.questions[1].question_id == "q-def"
    assert response.questions[1].text_to_evaluate == "What is an object?"
