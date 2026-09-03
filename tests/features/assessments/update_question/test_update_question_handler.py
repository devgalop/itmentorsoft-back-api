from unittest.mock import AsyncMock
import pytest

from src.features.assessments.update_question.update_question_handler import (
    UpdateQuestionHandler,
)
from src.features.assessments.update_question.update_question_request import (
    UpdateQuestionRequest,
)
from itmentorsoft_persistence.dto import (
    Question,
    QuestionRubricScore,
    QuestionStatus,
)

QUESTION_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"

VALID_UPDATE_REQUEST = dict(
    text="Updated text explaining polymorphism in OOP with clear examples",
    concept="Object Oriented Programming",
    definition="OOP is a programming paradigm based on objects and classes with updated definition",
    simple_explanation="OOP groups data and behavior together into reusable updated objects",
    correct_sample="Polymorphism allows objects of different types to be treated as instances of the same type",
    wrong_sample="Polymorphism means having many forms but it is not related to OOP at all",
    common_misconception=[
        "Polymorphism and inheritance are the exact same thing in OOP",
        "Polymorphism only works with interfaces and not with abstract classes",
    ],
    rubric=[
        {"score": 3, "criteria": "Complete and correct answer with clear examples"}
    ],
    semantic_keywords=["OOP", "polymorphism"],
)


def make_question(question_id=QUESTION_ID):
    q = Question(
        text_to_evaluate="Old text about abstraction and encapsulation in OOP with enough length",
        concept="Object Oriented Programming Old",
        definition="Old definition of OOP paradigm based on objects and classes here",
        simple_explanation="Old simple explanation of OOP grouping data and behavior",
        correct_sample="Old correct sample about abstraction hiding implementation details here",
        wrong_sample="Old wrong sample saying they are the same thing completely here",
        common_misconception=[
            "Old misconception that abstraction and encapsulation are the same",
            "Old misconception that encapsulation only means private fields",
        ],
        rubric=[QuestionRubricScore(score=2, explanation="Partial correct answer")],
        semantic_keywords=["OOP", "old-keyword"],
        status=QuestionStatus.DRAFT,
    )
    q.update_question_id(question_id)
    return q


@pytest.mark.asyncio
async def test_when_question_exists_then_should_update_successfully():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=make_question())
    question_repository.update_question = AsyncMock()

    handler = UpdateQuestionHandler(question_repository)

    request = UpdateQuestionRequest(**VALID_UPDATE_REQUEST)
    response = await handler.handle(QUESTION_ID, request)

    assert response.is_success is True
    question_repository.update_question.assert_called_once()


@pytest.mark.asyncio
async def test_when_question_does_not_exist_then_should_return_failure():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=None)

    handler = UpdateQuestionHandler(question_repository)

    request = UpdateQuestionRequest(**VALID_UPDATE_REQUEST)
    response = await handler.handle(QUESTION_ID, request)

    assert response.is_success is False
    assert response.message == "Question not found"
    question_repository.update_question.assert_not_called()


@pytest.mark.asyncio
async def test_when_update_is_successful_then_should_return_success_message():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=make_question())
    question_repository.update_question = AsyncMock()

    handler = UpdateQuestionHandler(question_repository)

    request = UpdateQuestionRequest(**VALID_UPDATE_REQUEST)
    response = await handler.handle(QUESTION_ID, request)

    assert response.is_success is True
    assert response.message == "Question updated successfully"


@pytest.mark.asyncio
async def test_when_repository_raises_exception_then_should_return_failure():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(
        side_effect=Exception("DB error")
    )

    handler = UpdateQuestionHandler(question_repository)

    request = UpdateQuestionRequest(**VALID_UPDATE_REQUEST)
    response = await handler.handle(QUESTION_ID, request)

    assert response.is_success is False
    assert "Failed to update question" in response.message


@pytest.mark.asyncio
async def test_calls_update_question_with_updated_fields():
    question_repository = AsyncMock()
    question_repository.get_question_rubric = AsyncMock(return_value=make_question())
    question_repository.update_question = AsyncMock()

    handler = UpdateQuestionHandler(question_repository)

    request = UpdateQuestionRequest(**VALID_UPDATE_REQUEST)
    await handler.handle(QUESTION_ID, request)

    call_args = question_repository.update_question.call_args
    updated_question = call_args[0][0]

    assert updated_question.text_to_evaluate == VALID_UPDATE_REQUEST["text"]
    assert updated_question.concept == VALID_UPDATE_REQUEST["concept"]
    assert updated_question.definition == VALID_UPDATE_REQUEST["definition"]
    assert (
        updated_question.simple_explanation
        == VALID_UPDATE_REQUEST["simple_explanation"]
    )
    assert updated_question.correct_sample == VALID_UPDATE_REQUEST["correct_sample"]
    assert updated_question.wrong_sample == VALID_UPDATE_REQUEST["wrong_sample"]
    assert (
        updated_question.common_misconception
        == VALID_UPDATE_REQUEST["common_misconception"]
    )
    assert (
        updated_question.semantic_keywords == VALID_UPDATE_REQUEST["semantic_keywords"]
    )
    assert len(updated_question.rubric) == 1
    assert updated_question.rubric[0].score == 3
    assert (
        updated_question.rubric[0].explanation
        == VALID_UPDATE_REQUEST["rubric"][0]["criteria"]
    )
