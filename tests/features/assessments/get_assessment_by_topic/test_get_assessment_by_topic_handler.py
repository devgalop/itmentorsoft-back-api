from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_handler import (
    GetAssessmentByTopicHandler,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_request import (
    GetAssessmentByTopicRequest,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_response import (
    EvaluativeQuestionDataByTopic,
    GetAssessmentByTopicResponse,
)

STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
TOPIC_ID = "topic-a1b2c3d4e5f6a7b8c9d0e1f2"
NUMBER_OF_QUESTIONS = 6


def make_question(
    question_id: str, text: str, topic: str = "test-topic"
) -> EvaluativeQuestionDataByTopic:
    return EvaluativeQuestionDataByTopic(
        question_id=question_id, text_to_evaluate=text, topic=topic
    )


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_return_assessment_successfully():
    questions = [
        make_question("q1", "What is OOP?"),
        make_question("q2", "Explain encapsulation"),
    ]

    service = AsyncMock()
    service.generate_assessment_by_topic = AsyncMock(
        return_value=GetAssessmentByTopicResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            topic_id=TOPIC_ID,
            questions=questions,
        )
    )

    handler = GetAssessmentByTopicHandler(service)

    request = GetAssessmentByTopicRequest(
        topic_id=TOPIC_ID,
        student_id=STUDENT_ID,
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Assessment retrieved successfully"
    assert response.assessment_id is not None
    assert response.questions is not None
    assert len(response.questions) == 2


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_return_questions():
    questions = [
        make_question("q1", "What is OOP?", topic=TOPIC_ID),
        make_question("q2", "Explain encapsulation", topic=TOPIC_ID),
        make_question("q3", "Define inheritance", topic=TOPIC_ID),
    ]

    service = AsyncMock()
    service.generate_assessment_by_topic = AsyncMock(
        return_value=GetAssessmentByTopicResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            topic_id=TOPIC_ID,
            questions=questions,
        )
    )

    handler = GetAssessmentByTopicHandler(service)

    request = GetAssessmentByTopicRequest(
        topic_id=TOPIC_ID,
        student_id=STUDENT_ID,
    )
    response = await handler.handle(request)

    assert response.questions is not None
    assert response.questions[0].question_id == "q1"
    assert response.questions[0].text_to_evaluate == "What is OOP?"
    assert response.questions[0].topic == TOPIC_ID
    assert response.questions[1].question_id == "q2"
    assert response.questions[2].question_id == "q3"


@pytest.mark.asyncio
async def test_when_service_raises_exception_then_should_return_failure():
    service = AsyncMock()
    service.generate_assessment_by_topic = AsyncMock(side_effect=Exception("DB error"))

    handler = GetAssessmentByTopicHandler(service)

    request = GetAssessmentByTopicRequest(
        topic_id=TOPIC_ID,
        student_id=STUDENT_ID,
    )
    response = await handler.handle(request)

    assert response.is_success is False
    assert "No se pudo obtener la evaluación" in response.message
    assert response.assessment_id is None
    assert response.questions is None


@pytest.mark.asyncio
async def test_when_request_is_valid_then_should_call_service_with_request():
    questions = [make_question("q1", "What is OOP?")]

    service = AsyncMock()
    service.generate_assessment_by_topic = AsyncMock(
        return_value=GetAssessmentByTopicResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            topic_id=TOPIC_ID,
            questions=questions,
        )
    )

    handler = GetAssessmentByTopicHandler(service)

    request = GetAssessmentByTopicRequest(
        topic_id=TOPIC_ID,
        student_id=STUDENT_ID,
    )
    await handler.handle(request)

    service.generate_assessment_by_topic.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_when_assessment_success_then_assessment_id_is_string():
    questions = [make_question("q1", "What is OOP?")]

    service = AsyncMock()
    service.generate_assessment_by_topic = AsyncMock(
        return_value=GetAssessmentByTopicResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            topic_id=TOPIC_ID,
            questions=questions,
        )
    )

    handler = GetAssessmentByTopicHandler(service)

    request = GetAssessmentByTopicRequest(
        topic_id=TOPIC_ID,
        student_id=STUDENT_ID,
    )
    response = await handler.handle(request)

    assert response.assessment_id is not None
    assert isinstance(response.assessment_id, str)


@pytest.mark.asyncio
async def test_when_assessment_success_then_response_includes_topic_id():
    questions = [make_question("q1", "What is OOP?")]

    service = AsyncMock()
    service.generate_assessment_by_topic = AsyncMock(
        return_value=GetAssessmentByTopicResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id="test-assessment-id",
            topic_id=TOPIC_ID,
            questions=questions,
        )
    )

    handler = GetAssessmentByTopicHandler(service)

    request = GetAssessmentByTopicRequest(
        topic_id=TOPIC_ID,
        student_id=STUDENT_ID,
    )
    response = await handler.handle(request)

    assert response.topic_id is not None
    assert response.topic_id == TOPIC_ID
