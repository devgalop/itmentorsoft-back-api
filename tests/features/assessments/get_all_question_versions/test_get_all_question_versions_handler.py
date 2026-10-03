import pytest
from unittest.mock import AsyncMock

from itmentorsoft_persistence.dto import QuestionDetails

from src.features.assessments.get_all_question_versions.get_all_question_versions_handler import (
    GetAllQuestionVersionsHandler,
)
from src.features.assessments.get_all_question_versions.get_all_question_versions_request import (
    GetAllQuestionVersionsRequest,
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
    question_versions = make_question_details(3)
    question_repository = AsyncMock()
    question_repository.get_all_versions_by_question = AsyncMock(
        return_value=question_versions
    )

    handler = GetAllQuestionVersionsHandler(question_repository)
    request = GetAllQuestionVersionsRequest(question_id="question-123")
    result = await handler.handle(request)

    assert result.is_success is True
    assert result.message == "Versiones de la pregunta obtenidas exitosamente"
    assert len(result.questions) == 3
    assert result.total == 3
    question_repository.get_all_versions_by_question.assert_called_once_with(
        "question-123"
    )


@pytest.mark.asyncio
async def test_handle_empty_result():
    question_repository = AsyncMock()
    question_repository.get_all_versions_by_question = AsyncMock(return_value=[])

    handler = GetAllQuestionVersionsHandler(question_repository)
    request = GetAllQuestionVersionsRequest(question_id="question-123")
    result = await handler.handle(request)

    assert result.is_success is False
    assert result.message == "No se encontraron versiones de la pregunta"
    assert result.questions == []
    assert result.total == 0
    question_repository.get_all_versions_by_question.assert_called_once_with(
        "question-123"
    )


@pytest.mark.asyncio
async def test_handle_data_integrity():
    question_versions = make_question_details(2)
    question_repository = AsyncMock()
    question_repository.get_all_versions_by_question = AsyncMock(
        return_value=question_versions
    )

    handler = GetAllQuestionVersionsHandler(question_repository)
    request = GetAllQuestionVersionsRequest(question_id="question-123")
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


@pytest.mark.asyncio
async def test_handle_exception_propagation():
    question_repository = AsyncMock()
    question_repository.get_all_versions_by_question = AsyncMock(
        side_effect=Exception("Database error")
    )

    handler = GetAllQuestionVersionsHandler(question_repository)
    request = GetAllQuestionVersionsRequest(question_id="question-123")

    with pytest.raises(Exception, match="Database error"):
        await handler.handle(request)
