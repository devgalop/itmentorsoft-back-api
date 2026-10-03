from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_assessment.get_assessment_handler import (
    GetAssessmentHandler,
)
from src.features.assessments.get_assessment.get_assessment_request import (
    GetAssessmentRequest,
)
from src.features.assessments.get_assessment.get_assessment_response import (
    EvaluativeQuestionData,
    GetAssessmentResponse,
)

STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
NUMBER_OF_QUESTIONS = 6


def make_question(question_id: str, text: str) -> EvaluativeQuestionData:
    return EvaluativeQuestionData(question_id=question_id, text_to_evaluate=text)


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_return_assessment_successfully():
    questions = [
        make_question("q1", "What is OOP?"),
        make_question("q2", "Explain encapsulation"),
    ]

    service = AsyncMock()
    service.generate_assessment = AsyncMock(
        return_value=GetAssessmentResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            questions=questions,
        )
    )

    handler = GetAssessmentHandler(service)

    request = GetAssessmentRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Assessment retrieved successfully"
    assert response.assessment_id is not None
    assert response.questions is not None
    assert len(response.questions) == 2


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_return_questions():
    questions = [
        make_question("q1", "What is OOP?"),
        make_question("q2", "Explain encapsulation"),
        make_question("q3", "Define inheritance"),
    ]

    service = AsyncMock()
    service.generate_assessment = AsyncMock(
        return_value=GetAssessmentResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            questions=questions,
        )
    )

    handler = GetAssessmentHandler(service)

    request = GetAssessmentRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.questions is not None
    assert response.questions[0].question_id == "q1"
    assert response.questions[0].text_to_evaluate == "What is OOP?"
    assert response.questions[1].question_id == "q2"
    assert response.questions[2].question_id == "q3"


@pytest.mark.asyncio
async def test_when_service_raises_exception_then_should_return_failure():
    service = AsyncMock()
    service.generate_assessment = AsyncMock(side_effect=Exception("DB error"))

    handler = GetAssessmentHandler(service)

    request = GetAssessmentRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.is_success is False
    assert "No se pudo obtener la evaluación" in response.message
    assert response.assessment_id is None
    assert response.questions is None


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_call_service_with_request():
    questions = [make_question("q1", "What is OOP?")]

    service = AsyncMock()
    service.generate_assessment = AsyncMock(return_value=questions)

    handler = GetAssessmentHandler(service)

    request = GetAssessmentRequest(student_id=STUDENT_ID)
    await handler.handle(request)

    service.generate_assessment.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_assessment_success_then_assessment_id_is_string():
    questions = [make_question("q1", "What is OOP?")]

    service = AsyncMock()
    service.generate_assessment = AsyncMock(
        return_value=GetAssessmentResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            questions=questions,
        )
    )

    handler = GetAssessmentHandler(service)

    request = GetAssessmentRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.assessment_id is not None
    assert isinstance(response.assessment_id, str)
