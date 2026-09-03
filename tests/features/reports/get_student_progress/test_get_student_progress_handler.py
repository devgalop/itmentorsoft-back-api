from unittest.mock import AsyncMock
import pytest

from src.features.reports.get_student_progress.get_student_progress_handler import (
    GetStudentProgressHandler,
)
from src.features.reports.get_student_progress.get_student_progress_request import (
    GetStudentProgressRequest,
)
from src.features.reports.get_student_progress.get_student_progress_response import (
    GetStudentProgressResponse,
)
from itmentorsoft_persistence.dto import (
    HistoricalResult,
    StudentProgress,
    StudentProgressDetail,
)
from src.features.reports.shared.student_report_service import (
    GetProgressByTopic,
    StudentReportService,
)


@pytest.mark.asyncio
async def test_when_student_has_progress_should_return_progress():
    student_report_service = AsyncMock(spec=StudentReportService)
    historical_progress = StudentProgress(
        student_id="123e4567e89b12d3a456426614174000",
        classification="Intermediate",
        feedback="Keep up the good work! Focus on improving your Science knowledge.",
        historical_progress=[
            StudentProgressDetail(
                topic="Mathematics",
                result=[
                    HistoricalResult(topic="Mathematics", score=3, index=1),
                    HistoricalResult(topic="Mathematics", score=2, index=2),
                ],
            ),
            StudentProgressDetail(
                topic="Science",
                result=[
                    HistoricalResult(topic="Science", score=1, index=1),
                ],
            ),
        ],
    )
    student_report_service.get_student_progress = AsyncMock(
        return_value=GetProgressByTopic(
            is_success=True,
            message="Student progress retrieved successfully",
            historical_progress=historical_progress,
        )
    )
    handler = GetStudentProgressHandler(student_report_service)
    response = await handler.handle(
        GetStudentProgressRequest(student_id="123e4567e89b12d3a456426614174000")
    )
    assert isinstance(response, GetStudentProgressResponse)
    assert response.is_success
    assert response.message == "Student progress retrieved successfully"
    assert response.progress is not None
    assert response.progress.student_id == "123e4567e89b12d3a456426614174000"
    assert response.progress.classification == "Intermediate"
    assert len(response.progress.knowledge_profile) == 3
    assert response.progress.knowledge_profile[0].topic == "Mathematics"
    assert response.progress.knowledge_profile[0].score == 100.0
    assert response.progress.knowledge_profile[0].index == 1
    assert response.progress.knowledge_profile[1].topic == "Mathematics"
    assert response.progress.knowledge_profile[1].score == pytest.approx(
        66.66666666666667
    )
    assert response.progress.knowledge_profile[1].index == 2
    assert response.progress.knowledge_profile[2].topic == "Science"
    assert response.progress.knowledge_profile[2].score == pytest.approx(
        33.33333333333333
    )
    assert response.progress.knowledge_profile[2].index == 1
    student_report_service.get_student_progress.assert_called_once_with(
        "123e4567e89b12d3a456426614174000"
    )


@pytest.mark.asyncio
async def test_when_service_returns_failure_should_return_failure():
    student_report_service = AsyncMock(spec=StudentReportService)
    student_report_service.get_student_progress = AsyncMock(
        return_value=GetProgressByTopic(
            is_success=False,
            message="Student not found",
            historical_progress=None,
        )
    )
    handler = GetStudentProgressHandler(student_report_service)
    response = await handler.handle(
        GetStudentProgressRequest(student_id="nonexistent_id")
    )
    assert isinstance(response, GetStudentProgressResponse)
    assert not response.is_success
    assert response.message == "Student not found"
    assert response.progress is None
    student_report_service.get_student_progress.assert_called_once_with(
        "nonexistent_id"
    )


@pytest.mark.asyncio
async def test_when_service_returns_no_progress_should_return_failure():
    student_report_service = AsyncMock(spec=StudentReportService)
    student_report_service.get_student_progress = AsyncMock(
        return_value=GetProgressByTopic(
            is_success=True,
            message="Student progress not found",
            historical_progress=None,
        )
    )
    handler = GetStudentProgressHandler(student_report_service)
    response = await handler.handle(
        GetStudentProgressRequest(student_id="123e4567e89b12d3a456426614174000")
    )
    assert isinstance(response, GetStudentProgressResponse)
    assert not response.is_success
    assert response.message == "Student progress not found"
    assert response.progress is None
    student_report_service.get_student_progress.assert_called_once_with(
        "123e4567e89b12d3a456426614174000"
    )
