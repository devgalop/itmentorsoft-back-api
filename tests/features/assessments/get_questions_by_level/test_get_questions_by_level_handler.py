from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_questions_by_level.get_questions_by_level_handler import (
    GetQuestionsByLevelHandler,
)
from src.features.assessments.get_questions_by_level.get_questions_by_level_request import (
    GetQuestionsByLevelRequest,
)
from itmentorsoft_persistence.dto import (
    EvaluativeQuestion,
    QuestionDifficulty,
)

DIFFICULTY = "básico"


def make_questions(count: int = 2):
    return [
        EvaluativeQuestion(
            question_id=f"question_id_{i}",
            text_to_evaluate=f"Question text {i}",
            topic=f"topic_{i}",
        )
        for i in range(count)
    ]


@pytest.mark.asyncio
async def test_when_questions_exist_then_should_return_questions_successfully():
    question_repository = AsyncMock()
    question_repository.get_question_by_level = AsyncMock(return_value=make_questions())

    handler = GetQuestionsByLevelHandler(question_repository)

    request = GetQuestionsByLevelRequest(difficulty=DIFFICULTY)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Questions retrieved successfully"
    assert len(response.questions) == 2


@pytest.mark.asyncio
async def test_when_no_questions_exist_then_should_return_empty_list():
    question_repository = AsyncMock()
    question_repository.get_question_by_level = AsyncMock(return_value=[])

    handler = GetQuestionsByLevelHandler(question_repository)

    request = GetQuestionsByLevelRequest(difficulty=DIFFICULTY)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Questions retrieved successfully"
    assert response.questions == []


@pytest.mark.asyncio
async def test_when_questions_exist_then_should_return_full_question_data():
    question_repository = AsyncMock()
    question_repository.get_question_by_level = AsyncMock(return_value=make_questions())

    handler = GetQuestionsByLevelHandler(question_repository)

    request = GetQuestionsByLevelRequest(difficulty=DIFFICULTY)
    response = await handler.handle(request)

    assert response.questions[0].question_id == "question_id_0"
    assert response.questions[0].text_to_evaluate == "Question text 0"
    assert response.questions[1].question_id == "question_id_1"
    assert response.questions[1].text_to_evaluate == "Question text 1"


@pytest.mark.asyncio
async def test_calls_repository_with_correct_difficulty():
    question_repository = AsyncMock()
    question_repository.get_question_by_level = AsyncMock(return_value=make_questions())

    handler = GetQuestionsByLevelHandler(question_repository)

    request = GetQuestionsByLevelRequest(difficulty=DIFFICULTY)
    await handler.handle(request)

    question_repository.get_question_by_level.assert_called_once_with(
        QuestionDifficulty.EASY
    )


@pytest.mark.asyncio
async def test_when_repository_raises_then_should_return_failure():
    question_repository = AsyncMock()
    question_repository.get_question_by_level = AsyncMock(
        side_effect=Exception("Database error")
    )

    handler = GetQuestionsByLevelHandler(question_repository)

    request = GetQuestionsByLevelRequest(difficulty=DIFFICULTY)
    response = await handler.handle(request)

    assert response.is_success is False
    assert "An error occurred while retrieving questions" in response.message
    assert response.questions == []
