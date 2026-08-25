from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_assessments_summary.get_assessments_summary_handler import (
    GetAssessmentsSummaryHandler,
)
from src.features.assessments.get_assessments_summary.get_assessments_summary_request import (
    GetAssessmentsSummaryRequest,
)
from src.features.assessments.shared.assessment import (
    AssessmentSummary,
    PaginatedAssessmentSummary,
)


@pytest.mark.asyncio
async def test_when_student_has_assessments_should_return_success_summary():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessments_summary = AsyncMock(
        return_value=PaginatedAssessmentSummary(
            total_assessments=2,
            assessments=[
                AssessmentSummary(
                    assessment_id="assessment_1",
                    score=85.0,
                    date_taken="2023-09-01T10:00:00Z",
                    classification="Pass",
                    feedback="Good performance.",
                ),
                AssessmentSummary(
                    assessment_id="assessment_2",
                    score=70.0,
                    date_taken="2023-09-05T14:30:00Z",
                    classification="Pass",
                    feedback="Satisfactory performance.",
                ),
            ],
        )
    )

    handler = GetAssessmentsSummaryHandler(assessment_repository)
    response = await handler.handle(
        GetAssessmentsSummaryRequest(student_id="student_123", page=0, page_size=10)
    )

    assert response.is_success is True
    assert response.message == "Assessments summary retrieved successfully."
    assert response.total_assessments == 2
    assert len(response.assessments) == 2
    assert response.assessments[0].assessment_id == "assessment_1"
    assert response.assessments[0].score == 85.0
    assert response.assessments[1].assessment_id == "assessment_2"
    assert response.assessments[1].score == 70.0
    assessment_repository.get_assessments_summary.assert_called_once_with(
        "student_123", 0, 10
    )


@pytest.mark.asyncio
async def test_when_student_has_no_assessments_should_return_failure():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessments_summary = AsyncMock(
        return_value=PaginatedAssessmentSummary(
            total_assessments=0,
            assessments=[],
        )
    )

    handler = GetAssessmentsSummaryHandler(assessment_repository)
    response = await handler.handle(
        GetAssessmentsSummaryRequest(student_id="student_456", page=0, page_size=10)
    )

    assert response.is_success is False
    assert response.message == "No assessments found for the student."
    assert response.total_assessments == 0
    assert response.assessments == []
    assessment_repository.get_assessments_summary.assert_called_once_with(
        "student_456", 0, 10
    )


@pytest.mark.asyncio
async def test_when_repository_raises_error_should_propagate_exception():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessments_summary = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = GetAssessmentsSummaryHandler(assessment_repository)

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(GetAssessmentsSummaryRequest(student_id="student_789"))

    assessment_repository.get_assessments_summary.assert_called_once_with(
        "student_789", 0, 10
    )


@pytest.mark.asyncio
async def test_when_pagination_params_are_used_should_pass_to_repository():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessments_summary = AsyncMock(
        return_value=PaginatedAssessmentSummary(
            total_assessments=1,
            assessments=[
                AssessmentSummary(
                    assessment_id="assessment_1",
                    score=90.0,
                    date_taken="2023-10-01T10:00:00Z",
                )
            ],
        )
    )

    handler = GetAssessmentsSummaryHandler(assessment_repository)
    response = await handler.handle(
        GetAssessmentsSummaryRequest(student_id="student_123", page=2, page_size=5)
    )

    assert response.is_success is True
    assessment_repository.get_assessments_summary.assert_called_once_with(
        "student_123", 2, 5
    )


@pytest.mark.asyncio
async def test_when_assessment_has_optional_fields_none_should_map_correctly():
    assessment_repository = AsyncMock()
    assessment_repository.get_assessments_summary = AsyncMock(
        return_value=PaginatedAssessmentSummary(
            total_assessments=1,
            assessments=[
                AssessmentSummary(
                    assessment_id="assessment_1",
                    score=75.0,
                    date_taken="2023-09-15T08:00:00Z",
                )
            ],
        )
    )

    handler = GetAssessmentsSummaryHandler(assessment_repository)
    response = await handler.handle(
        GetAssessmentsSummaryRequest(student_id="student_123")
    )

    assert response.is_success is True
    assert response.assessments[0].classification is None
    assert response.assessments[0].feedback is None
    assert response.assessments[0].score == 75.0
