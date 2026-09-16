from unittest.mock import AsyncMock
import pytest

from src.features.assessments.register_question.register_question_handler import (
    RegisterQuestionHandler,
)
from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
from src.features.assessments.shared.question_manager_service import (
    CreateQuestionRequest,
    CreateQuestionResponse,
    QuestionManagerService,
)

VALID_REGISTER_REQUEST = dict(
    text="Explain the difference between abstraction and encapsulation in OOP",
    concept="Object Oriented Programming",
    definition="OOP is a programming paradigm based on objects and classes",
    simple_explanation="OOP groups data and behavior together into reusable objects",
    correct_sample="Abstraction hides implementation details while encapsulation bundles data",
    wrong_sample="They are the same thing, both hide data from the user completely",
    common_misconception=[
        "Abstraction and encapsulation are the same concept in OOP",
        "Encapsulation only refers to using private fields inside a class",
    ],
    rubric=[{"score": 3, "criteria": "Complete and correct answer with examples"}],
    semantic_keywords=["OOP", "abstraction"],
    difficulty="intermedio",
    topic="Object Oriented Programming",
)


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_register_question_successfully():
    question_service = AsyncMock(spec=QuestionManagerService)
    question_service.create_question = AsyncMock(
        return_value=CreateQuestionResponse(
            is_success=True,
            message="Question created successfully",
            question_id="abc123",
        )
    )

    handler = RegisterQuestionHandler(question_service)

    request = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    response = await handler.handle(request, "test_user")

    assert response.is_success is True
    assert response.message == "Question created successfully"
    question_service.create_question.assert_called_once()
    call_args = question_service.create_question.call_args[0][0]
    assert isinstance(call_args, CreateQuestionRequest)
    assert call_args.user_name == "test_user"


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_return_question_id_as_string():
    question_service = AsyncMock(spec=QuestionManagerService)
    question_service.create_question = AsyncMock(
        return_value=CreateQuestionResponse(
            is_success=True,
            message="Question created successfully",
            question_id="abc123",
        )
    )

    handler = RegisterQuestionHandler(question_service)

    request = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    response = await handler.handle(request, "test_user")

    assert response.question_id is not None
    assert isinstance(response.question_id, str)


@pytest.mark.asyncio
async def test_when_repository_raises_exception_then_should_return_failure():
    question_service = AsyncMock(spec=QuestionManagerService)
    question_service.create_question = AsyncMock(side_effect=Exception("DB error"))

    handler = RegisterQuestionHandler(question_service)

    request = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    response = await handler.handle(request, "test_user")

    assert response.is_success is False
    assert "Failed to register question" in response.message
    assert response.question_id is None
