from unittest.mock import AsyncMock
import pytest

from src.features.reports.get_student_summary.get_student_summary_handler import (
    GetStudentSummaryHandler,
)
from src.features.reports.get_student_summary.get_student_summary_request import (
    GetStudentSummaryRequest,
)
from itmentorsoft_persistence.dto import (
    StudentKnowledgeProfile,
    StudentSummary,
)
from src.features.reports.shared.student_report_service import GetSummaryResponse

STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def make_student_summary(
    student_id: str = STUDENT_ID,
    student_name: str = "Test Student",
    knowledge_profiles: list | None = None,
    knowledge_classification: str = "Advanced",
    feedback: str = "Good progress",
) -> StudentSummary:
    if knowledge_profiles is None:
        knowledge_profiles = [
            StudentKnowledgeProfile(topic="Mathematics", score=3),
            StudentKnowledgeProfile(topic="Science", score=2),
        ]
    return StudentSummary(
        student_id=student_id,
        student_name=student_name,
        knowledge_profiles=knowledge_profiles,
        knowledge_classification=knowledge_classification,
        feedback=feedback,
    )


@pytest.mark.asyncio
async def test_when_student_exists_then_return_success_with_summary():
    service = AsyncMock()
    service.get_student_summary = AsyncMock(
        return_value=GetSummaryResponse(
            is_success=True,
            message="Student summary retrieved successfully",
            student_summary=make_student_summary(),
        )
    )

    handler = GetStudentSummaryHandler(service)
    request = GetStudentSummaryRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Student summary retrieved successfully"
    assert response.summary is not None
    assert response.summary.student_id == STUDENT_ID
    assert response.summary.name == "Test Student"
    assert response.summary.knowledge_classification == "Advanced"
    assert response.summary.feedback == "Good progress"
    assert len(response.summary.profile) == 2


@pytest.mark.asyncio
async def test_when_student_not_found_then_return_failure():
    service = AsyncMock()
    service.get_student_summary = AsyncMock(
        return_value=GetSummaryResponse(
            is_success=False,
            message="Student not found",
            student_summary=None,
        )
    )

    handler = GetStudentSummaryHandler(service)
    request = GetStudentSummaryRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Student not found"
    assert response.summary is None


@pytest.mark.asyncio
async def test_when_summary_not_found_then_return_failure():
    service = AsyncMock()
    service.get_student_summary = AsyncMock(
        return_value=GetSummaryResponse(
            is_success=False,
            message="Student summary not found",
            student_summary=None,
        )
    )

    handler = GetStudentSummaryHandler(service)
    request = GetStudentSummaryRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Student summary not found"
    assert response.summary is None


@pytest.mark.asyncio
async def test_when_service_returns_success_but_no_summary_then_return_failure():
    service = AsyncMock()
    service.get_student_summary = AsyncMock(
        return_value=GetSummaryResponse(
            is_success=True,
            message="Student summary retrieved successfully",
            student_summary=None,
        )
    )

    handler = GetStudentSummaryHandler(service)
    request = GetStudentSummaryRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.summary is None


@pytest.mark.asyncio
async def test_map_to_response_converts_knowledge_profiles_correctly():
    service = AsyncMock()
    profiles = [
        StudentKnowledgeProfile(topic="Mathematics", score=3),
        StudentKnowledgeProfile(topic="Science", score=2),
        StudentKnowledgeProfile(topic="History", score=1),
    ]
    service.get_student_summary = AsyncMock(
        return_value=GetSummaryResponse(
            is_success=True,
            message="Student summary retrieved successfully",
            student_summary=make_student_summary(knowledge_profiles=profiles),
        )
    )

    handler = GetStudentSummaryHandler(service)
    request = GetStudentSummaryRequest(student_id=STUDENT_ID)
    response = await handler.handle(request)

    assert response.summary.profile[0].topic == "Mathematics"
    assert response.summary.profile[0].score == 100.0  # (3/3)*100
    assert response.summary.profile[1].topic == "Science"
    assert response.summary.profile[1].score == pytest.approx(
        66.66666666666667
    )  # (2/3)*100
    assert response.summary.profile[2].topic == "History"
    assert response.summary.profile[2].score == pytest.approx(
        33.33333333333333
    )  # (1/3)*100


@pytest.mark.asyncio
async def test_handler_calls_service_with_correct_student_id():
    service = AsyncMock()
    service.get_student_summary = AsyncMock(
        return_value=GetSummaryResponse(
            is_success=True,
            message="Student summary retrieved successfully",
            student_summary=make_student_summary(),
        )
    )

    handler = GetStudentSummaryHandler(service)
    request = GetStudentSummaryRequest(student_id=STUDENT_ID)
    await handler.handle(request)

    service.get_student_summary.assert_called_once_with(STUDENT_ID)
