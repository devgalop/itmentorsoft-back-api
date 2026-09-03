from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_question_by_id.get_question_by_id_handler import (
    GetQuestionByIdHandler,
)
from src.features.assessments.get_question_by_id.get_question_by_id_request import (
    GetQuestionByIdRequest,
)
from itmentorsoft_persistence.dto import (
    Question,
    QuestionRubricScore,
    QuestionStatus,
)

QUESTION_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def make_question(question_id: str = QUESTION_ID):
    q = Question(
        text_to_evaluate="Explain the difference between abstraction and encapsulation in OOP",
        concept="Object Oriented Programming",
        definition="OOP is a programming paradigm based on objects",
        simple_explanation="OOP groups data and behavior into objects",
        correct_sample="Abstraction hides implementation details while encapsulation bundles data",
        wrong_sample="They are the same thing, both hide data from users",
        common_misconception=[
            "Abstraction and encapsulation are the same concept",
            "Encapsulation only refers to private fields in a class",
        ],
        rubric=[QuestionRubricScore(score=3, explanation="Complete correct answer")],
        semantic_keywords=["OOP", "abstraction", "encapsulation"],
        status=QuestionStatus.DRAFT,
    )
    q.update_question_id(question_id)
    return q


@pytest.mark.asyncio
async def test_when_question_exists_then_should_return_question_successfully():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=make_question())

    handler = GetQuestionByIdHandler(question_repository)

    request = GetQuestionByIdRequest(question_id=QUESTION_ID)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Question retrieved successfully"
    assert response.question is not None


@pytest.mark.asyncio
async def test_when_question_does_not_exist_then_should_return_failure():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=None)

    handler = GetQuestionByIdHandler(question_repository)

    request = GetQuestionByIdRequest(question_id=QUESTION_ID)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Question not found"
    assert response.question is None


@pytest.mark.asyncio
async def test_when_question_exists_then_should_return_full_question_data():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=make_question())

    handler = GetQuestionByIdHandler(question_repository)

    request = GetQuestionByIdRequest(question_id=QUESTION_ID)
    response = await handler.handle(request)

    q = response.question
    assert q is not None
    assert q.question_id == QUESTION_ID
    assert (
        q.text == "Explain the difference between abstraction and encapsulation in OOP"
    )
    assert q.concept == "Object Oriented Programming"
    assert q.definition == "OOP is a programming paradigm based on objects"
    assert q.simple_explanation == "OOP groups data and behavior into objects"
    assert (
        q.correct_sample
        == "Abstraction hides implementation details while encapsulation bundles data"
    )
    assert q.wrong_sample == "They are the same thing, both hide data from users"
    assert q.common_misconception == [
        "Abstraction and encapsulation are the same concept",
        "Encapsulation only refers to private fields in a class",
    ]
    assert q.semantic_keywords == ["OOP", "abstraction", "encapsulation"]
    assert q.status == "draft"


@pytest.mark.asyncio
async def test_when_question_exists_then_should_return_rubric_data():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=make_question())

    handler = GetQuestionByIdHandler(question_repository)

    request = GetQuestionByIdRequest(question_id=QUESTION_ID)
    response = await handler.handle(request)

    assert response.question is not None
    assert len(response.question.rubric) == 1
    assert response.question.rubric[0].score == 3
    assert response.question.rubric[0].explanation == "Complete correct answer"


@pytest.mark.asyncio
async def test_calls_repository_with_correct_question_id():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=make_question())

    handler = GetQuestionByIdHandler(question_repository)

    request = GetQuestionByIdRequest(question_id=QUESTION_ID)
    await handler.handle(request)

    question_repository.get_question_rubric.assert_called_once_with(QUESTION_ID)
