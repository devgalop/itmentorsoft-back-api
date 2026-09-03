from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_assessment_result.get_assessment_result_handler import (
    GetAssessmentResultHandler,
)
from src.features.assessments.get_assessment_result.get_assessment_result_request import (
    GetAssessmentResultRequest,
)
from itmentorsoft_persistence.dto import (
    StudentAnswerScore,
    StudentAssessmentResult,
)


@pytest.mark.asyncio
async def test_when_assessment_result_exists_should_return_success():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessment_result = AsyncMock(
        return_value=StudentAssessmentResult(
            assessment_id="assessment_123",
            student_id="user_456",
            avg_score=85.5,
            classification="Pass",
            feedback="Good performance",
            answer_scores=[
                StudentAnswerScore(
                    question_id="q1",
                    question_text="What is 2+2?",
                    answer="4",
                    score=10.0,
                    feedback="Correct",
                    misconceptions=None,
                    key_concepts=["Mathematics", "Addition"],
                )
            ],
        )
    )

    handler = GetAssessmentResultHandler(assessment_repository)
    request = GetAssessmentResultRequest(
        assessment_id="assessment_123", user_id="user_456"
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Assessment result retrieved successfully."
    assert response.result is not None
    assert response.result.assessment_id == "assessment_123"
    assert response.result.user_id == "user_456"
    assert response.result.avg_score == 85.5
    assert response.result.classification == "Pass"
    assert response.result.feedback == "Good performance"
    assert len(response.result.answer_scores) == 1
    assert response.result.answer_scores[0].question_id == "q1"
    assert response.result.answer_scores[0].score == 10.0
    assessment_repository.get_assessment_result.assert_called_once_with(
        "assessment_123", "user_456"
    )


@pytest.mark.asyncio
async def test_when_assessment_result_not_found_should_return_failure():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessment_result = AsyncMock(return_value=None)

    handler = GetAssessmentResultHandler(assessment_repository)
    request = GetAssessmentResultRequest(
        assessment_id="nonexistent", user_id="user_456"
    )
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Assessment result not found."
    assert response.result is None
    assessment_repository.get_assessment_result.assert_called_once_with(
        "nonexistent", "user_456"
    )


@pytest.mark.asyncio
async def test_when_multiple_answer_scores_should_return_all():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessment_result = AsyncMock(
        return_value=StudentAssessmentResult(
            assessment_id="assessment_789",
            student_id="user_101",
            avg_score=72.3,
            classification="Needs Improvement",
            feedback="Keep studying",
            answer_scores=[
                StudentAnswerScore(
                    question_id="q1",
                    question_text="Question 1",
                    answer="Answer 1",
                    score=8.0,
                    feedback="Good",
                    misconceptions=None,
                    key_concepts=["Concept A"],
                ),
                StudentAnswerScore(
                    question_id="q2",
                    question_text="Question 2",
                    answer="Answer 2",
                    score=6.0,
                    feedback="Fair",
                    misconceptions=["Misconception 1"],
                    key_concepts=["Concept B", "Concept C"],
                ),
            ],
        )
    )

    handler = GetAssessmentResultHandler(assessment_repository)
    request = GetAssessmentResultRequest(
        assessment_id="assessment_789", user_id="user_101"
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.result is not None
    assert len(response.result.answer_scores) == 2
    assert response.result.answer_scores[0].question_id == "q1"
    assert response.result.answer_scores[1].question_id == "q2"
    assert response.result.answer_scores[1].misconceptions == ["Misconception 1"]
    assert response.result.answer_scores[1].key_concepts == ["Concept B", "Concept C"]
