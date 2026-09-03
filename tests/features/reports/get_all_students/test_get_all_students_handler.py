from unittest.mock import AsyncMock
import pytest

from src.features.reports.get_all_students.get_all_students_handler import (
    GetAllStudentsHandler,
)
from src.features.reports.get_all_students.get_all_students_request import (
    GetAllStudentsRequest,
)
from src.features.reports.get_all_students.get_all_students_response import (
    GetAllStudentsResponse,
)
from itmentorsoft_persistence.dto import (
    PaginatedStudentSummary,
    StudentBasicSummary,
)
from src.features.reports.shared.student_report_service import (
    GetStudentsResponse,
    StudentReportService,
)


def make_paginated_summary(
    students: list | None = None,
    total_students: int = 2,
    page: int = 0,
) -> PaginatedStudentSummary:
    if students is None:
        students = [
            StudentBasicSummary(
                student_id="123e4567e89b12d3a456426614174000",
                student_name="Alice",
                knowledge_classification="Advanced",
            ),
            StudentBasicSummary(
                student_id="456e7890e12b34d5a678901234567890",
                student_name="Bob",
                knowledge_classification="Beginner",
            ),
        ]
    return PaginatedStudentSummary(
        students=students, total_students=total_students, page=page
    )


@pytest.mark.asyncio
async def test_when_students_exist_then_return_success_with_result():
    service = AsyncMock(spec=StudentReportService)
    service.get_all_students = AsyncMock(
        return_value=GetStudentsResponse(
            is_success=True,
            message="Students retrieved successfully",
            students=make_paginated_summary(),
        )
    )

    handler = GetAllStudentsHandler(service)
    response = await handler.handle(GetAllStudentsRequest(page=0, page_size=10))

    assert isinstance(response, GetAllStudentsResponse)
    assert response.is_success is True
    assert response.message == "Students retrieved successfully"
    assert response.result is not None
    assert len(response.result.students) == 2
    assert response.result.total_students == 2
    assert response.result.page == 0
    assert response.result.students[0].student_id == "123e4567e89b12d3a456426614174000"
    assert response.result.students[0].student_name == "Alice"
    assert response.result.students[0].knowledge_classification == "Advanced"
    assert response.result.students[1].student_id == "456e7890e12b34d5a678901234567890"
    assert response.result.students[1].student_name == "Bob"
    assert response.result.students[1].knowledge_classification == "Beginner"


@pytest.mark.asyncio
async def test_when_service_returns_failure_then_return_failure():
    service = AsyncMock(spec=StudentReportService)
    service.get_all_students = AsyncMock(
        return_value=GetStudentsResponse(
            is_success=False,
            message="Students not found",
            students=None,
        )
    )

    handler = GetAllStudentsHandler(service)
    response = await handler.handle(GetAllStudentsRequest(page=0, page_size=10))

    assert isinstance(response, GetAllStudentsResponse)
    assert response.is_success is False
    assert response.message == "Students not found"
    assert response.result is None


@pytest.mark.asyncio
async def test_when_service_returns_success_but_no_students_then_return_no_result():
    service = AsyncMock(spec=StudentReportService)
    service.get_all_students = AsyncMock(
        return_value=GetStudentsResponse(
            is_success=True,
            message="Students retrieved successfully",
            students=None,
        )
    )

    handler = GetAllStudentsHandler(service)
    response = await handler.handle(GetAllStudentsRequest(page=0, page_size=10))

    assert isinstance(response, GetAllStudentsResponse)
    assert response.is_success is True
    assert response.result is None


@pytest.mark.asyncio
async def test_when_service_returns_empty_student_list_then_return_empty_result():
    service = AsyncMock(spec=StudentReportService)
    service.get_all_students = AsyncMock(
        return_value=GetStudentsResponse(
            is_success=True,
            message="Students retrieved successfully",
            students=make_paginated_summary(students=[], total_students=0, page=0),
        )
    )

    handler = GetAllStudentsHandler(service)
    response = await handler.handle(GetAllStudentsRequest(page=0, page_size=10))

    assert isinstance(response, GetAllStudentsResponse)
    assert response.is_success is True
    assert response.result is not None
    assert len(response.result.students) == 0
    assert response.result.total_students == 0


@pytest.mark.asyncio
async def test_map_to_response_converts_students_correctly():
    service = AsyncMock(spec=StudentReportService)
    students = [
        StudentBasicSummary(
            student_id="aaa111",
            student_name="Charlie",
            knowledge_classification="Intermediate",
        ),
        StudentBasicSummary(
            student_id="bbb222",
            student_name="Diana",
            knowledge_classification="Advanced",
        ),
        StudentBasicSummary(
            student_id="ccc333",
            student_name="Eve",
            knowledge_classification="Beginner",
        ),
    ]
    service.get_all_students = AsyncMock(
        return_value=GetStudentsResponse(
            is_success=True,
            message="Students retrieved successfully",
            students=make_paginated_summary(
                students=students, total_students=3, page=1
            ),
        )
    )

    handler = GetAllStudentsHandler(service)
    response = await handler.handle(GetAllStudentsRequest(page=1, page_size=10))

    assert response.result.total_students == 3
    assert response.result.page == 1
    assert len(response.result.students) == 3
    assert response.result.students[0].student_name == "Charlie"
    assert response.result.students[0].knowledge_classification == "Intermediate"
    assert response.result.students[1].student_name == "Diana"
    assert response.result.students[1].knowledge_classification == "Advanced"
    assert response.result.students[2].student_name == "Eve"
    assert response.result.students[2].knowledge_classification == "Beginner"


@pytest.mark.asyncio
async def test_handler_calls_service_with_correct_pagination():
    service = AsyncMock(spec=StudentReportService)
    service.get_all_students = AsyncMock(
        return_value=GetStudentsResponse(
            is_success=True,
            message="Students retrieved successfully",
            students=make_paginated_summary(),
        )
    )

    handler = GetAllStudentsHandler(service)
    await handler.handle(GetAllStudentsRequest(page=2, page_size=25))

    service.get_all_students.assert_called_once_with(2, 25)
