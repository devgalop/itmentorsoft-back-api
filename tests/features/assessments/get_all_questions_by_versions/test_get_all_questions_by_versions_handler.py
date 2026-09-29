import pytest
from unittest.mock import AsyncMock

from itmentorsoft_persistence.dto import QuestionDetails, PaginatedQuestionsResult

from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_handler import (
    GetAllQuestionsByVersionsHandler,
)
from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_request import (
    GetAllQuestionsByVersionsRequest,
)


def make_question_details(count: int = 2) -> list[QuestionDetails]:
    return [
        QuestionDetails(
            question_id=f"q{i}",
            text_to_evaluate=f"Text to evaluate {i}",
            concept=f"Concept {i}",
            definition=f"Definition {i}",
            simple_explanation=f"Simple explanation {i}",
            correct_sample=f"Correct sample {i}",
            wrong_sample=f"Wrong sample {i}",
            status="ACTIVE",
            difficulty="MEDIUM",
            classification="CATEGORY_A",
            version=i,
        )
        for i in range(1, count + 1)
    ]


@pytest.mark.asyncio
async def test_handle_success():
    questions = make_question_details(3)
    paginated_result = PaginatedQuestionsResult(items=questions, total=3)
    question_repository = AsyncMock()
    question_repository.get_latest_versions_all_questions = AsyncMock(
        return_value=paginated_result
    )

    handler = GetAllQuestionsByVersionsHandler(question_repository)
    request = GetAllQuestionsByVersionsRequest(page=0, page_size=10)
    result = await handler.handle(request)

    assert result.is_success is True
    assert result.message == "Questions retrieved successfully"
    assert len(result.questions) == 3
    assert result.total == 3
    question_repository.get_latest_versions_all_questions.assert_called_once_with(
        page=0, page_size=10
    )


@pytest.mark.asyncio
async def test_handle_empty_result():
    paginated_result = PaginatedQuestionsResult(items=[], total=0)
    question_repository = AsyncMock()
    question_repository.get_latest_versions_all_questions = AsyncMock(
        return_value=paginated_result
    )

    handler = GetAllQuestionsByVersionsHandler(question_repository)
    request = GetAllQuestionsByVersionsRequest(page=0, page_size=10)
    result = await handler.handle(request)

    assert result.is_success is False
    assert result.message == "No questions found"
    assert result.questions == []
    assert result.total == 0
    question_repository.get_latest_versions_all_questions.assert_called_once_with(
        page=0, page_size=10
    )


@pytest.mark.asyncio
async def test_handle_data_integrity():
    questions = make_question_details(2)
    paginated_result = PaginatedQuestionsResult(items=questions, total=2)
    question_repository = AsyncMock()
    question_repository.get_latest_versions_all_questions = AsyncMock(
        return_value=paginated_result
    )

    handler = GetAllQuestionsByVersionsHandler(question_repository)
    request = GetAllQuestionsByVersionsRequest(page=1, page_size=20)
    result = await handler.handle(request)

    assert result.questions[0].question_id == "q1"
    assert result.questions[0].text_to_evaluate == "Text to evaluate 1"
    assert result.questions[0].concept == "Concept 1"
    assert result.questions[0].definition == "Definition 1"
    assert result.questions[0].simple_explanation == "Simple explanation 1"
    assert result.questions[0].correct_sample == "Correct sample 1"
    assert result.questions[0].wrong_sample == "Wrong sample 1"
    assert result.questions[0].status == "ACTIVE"
    assert result.questions[0].difficulty == "MEDIUM"
    assert result.questions[0].classification == "CATEGORY_A"
    assert result.questions[0].version == 1
    assert result.questions[1].question_id == "q2"
    assert result.questions[1].version == 2
    question_repository.get_latest_versions_all_questions.assert_called_once_with(
        page=1, page_size=20
    )


@pytest.mark.asyncio
async def test_handle_exception_propagation():
    question_repository = AsyncMock()
    question_repository.get_latest_versions_all_questions = AsyncMock(
        side_effect=Exception("Database error")
    )

    handler = GetAllQuestionsByVersionsHandler(question_repository)
    request = GetAllQuestionsByVersionsRequest(page=0, page_size=10)

    with pytest.raises(Exception, match="Database error"):
        await handler.handle(request)
