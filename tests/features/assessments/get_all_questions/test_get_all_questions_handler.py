from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_all_questions.get_all_questions_handler import (
    GetAllQuestionsHandler,
)
from src.features.assessments.get_all_questions.get_all_questions_request import (
    GetAllQuestionsRequest,
)
from itmentorsoft_persistence.dto import PaginatedQuestionsResult
from itmentorsoft_persistence.dto import QuestionDetails


def make_question_details(count: int = 2):
    return [
        QuestionDetails(
            question_id=f"question_id_{i}",
            text_to_evaluate=f"Question text {i}",
            concept=f"Concept {i}",
            definition=f"Definition {i}",
            simple_explanation=f"Explanation {i}",
            correct_sample=f"Correct {i}",
            wrong_sample=f"Wrong {i}",
            status="published",
            difficulty="básico",
            classification=f"Classification {i}",
            version=1,
        )
        for i in range(count)
    ]


@pytest.mark.asyncio
async def test_when_questions_exist_then_should_return_questions_successfully():
    question_repository = AsyncMock()
    items = make_question_details()
    question_repository.get_all_questions_paginated = AsyncMock(
        return_value=PaginatedQuestionsResult(items=items, total=100)
    )

    handler = GetAllQuestionsHandler(question_repository)

    request = GetAllQuestionsRequest(page=0, page_size=10)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Successfully retrieved all questions."
    assert len(response.questions) == 2
    assert response.total == 100


@pytest.mark.asyncio
async def test_when_no_questions_exist_then_should_return_empty_list():
    question_repository = AsyncMock()
    question_repository.get_all_questions_paginated = AsyncMock(
        return_value=PaginatedQuestionsResult(items=[], total=0)
    )

    handler = GetAllQuestionsHandler(question_repository)

    request = GetAllQuestionsRequest(page=0, page_size=10)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "No questions found."
    assert response.questions == []
    assert response.total == 0


@pytest.mark.asyncio
async def test_when_questions_exist_then_should_return_full_question_data():
    question_repository = AsyncMock()
    items = make_question_details()
    question_repository.get_all_questions_paginated = AsyncMock(
        return_value=PaginatedQuestionsResult(items=items, total=2)
    )

    handler = GetAllQuestionsHandler(question_repository)

    request = GetAllQuestionsRequest(page=0, page_size=10)
    response = await handler.handle(request)

    assert response.questions[0].question_id == "question_id_0"
    assert response.questions[0].text_to_evaluate == "Question text 0"
    assert response.questions[0].concept == "Concept 0"
    assert response.questions[1].question_id == "question_id_1"
    assert response.questions[1].text_to_evaluate == "Question text 1"


@pytest.mark.asyncio
async def test_calls_repository_with_correct_page_and_page_size():
    question_repository = AsyncMock()
    items = make_question_details()
    question_repository.get_all_questions_paginated = AsyncMock(
        return_value=PaginatedQuestionsResult(items=items, total=2)
    )

    handler = GetAllQuestionsHandler(question_repository)

    request = GetAllQuestionsRequest(page=3, page_size=25)
    await handler.handle(request)

    question_repository.get_all_questions_paginated.assert_called_once_with(3, 25)


@pytest.mark.asyncio
async def test_when_repository_raises_then_exception_propagates():
    question_repository = AsyncMock()
    question_repository.get_all_questions_paginated = AsyncMock(
        side_effect=Exception("Database error")
    )

    handler = GetAllQuestionsHandler(question_repository)

    request = GetAllQuestionsRequest(page=0, page_size=10)

    with pytest.raises(Exception, match="Database error"):
        await handler.handle(request)
