from unittest.mock import AsyncMock
import pytest

from src.features.reports.get_all_students_by_category.get_all_students_by_category_handler import (
    GetStudentsByCategoryHandler,
)
from src.features.reports.get_all_students_by_category.get_all_students_by_category_request import (
    GetStudentsByCategoryRequest,
)
from src.features.reports.get_all_students_by_category.get_all_students_by_category_response import (
    GetStudentsByCategoryResponse,
)
from itmentorsoft_persistence.repositories import ReportRepository
from itmentorsoft_persistence.dto import (
    PaginatedStudentSummary,
    StudentBasicSummary,
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
                knowledge_classification="Advanced",
            ),
        ]
    return PaginatedStudentSummary(
        students=students, total_students=total_students, page=page
    )


@pytest.mark.asyncio
async def test_when_students_exist_then_return_success_with_result():
    repository = AsyncMock(spec=ReportRepository)
    repository.get_all_students_by_category = AsyncMock(
        return_value=make_paginated_summary()
    )

    handler = GetStudentsByCategoryHandler(repository)
    response = await handler.handle(
        GetStudentsByCategoryRequest(category="Advanced", page=0, page_size=10)
    )

    assert isinstance(response, GetStudentsByCategoryResponse)
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
    assert response.result.students[1].knowledge_classification == "Advanced"


@pytest.mark.asyncio
async def test_when_no_students_found_then_return_empty_result():
    repository = AsyncMock(spec=ReportRepository)
    repository.get_all_students_by_category = AsyncMock(
        return_value=make_paginated_summary(students=[], total_students=0, page=0)
    )

    handler = GetStudentsByCategoryHandler(repository)
    response = await handler.handle(
        GetStudentsByCategoryRequest(category="Unknown", page=0, page_size=10)
    )

    assert isinstance(response, GetStudentsByCategoryResponse)
    assert response.is_success is True
    assert response.result is not None
    assert len(response.result.students) == 0
    assert response.result.total_students == 0


@pytest.mark.asyncio
async def test_map_to_response_converts_students_correctly():
    repository = AsyncMock(spec=ReportRepository)
    students = [
        StudentBasicSummary(
            student_id="aaa111",
            student_name="Charlie",
            knowledge_classification="Beginner",
        ),
        StudentBasicSummary(
            student_id="bbb222",
            student_name="Diana",
            knowledge_classification="Intermediate",
        ),
        StudentBasicSummary(
            student_id="ccc333",
            student_name="Eve",
            knowledge_classification="Advanced",
        ),
    ]
    repository.get_all_students_by_category = AsyncMock(
        return_value=make_paginated_summary(students=students, total_students=3, page=1)
    )

    handler = GetStudentsByCategoryHandler(repository)
    response = await handler.handle(
        GetStudentsByCategoryRequest(category="Beginner", page=1, page_size=10)
    )

    assert response.result.total_students == 3
    assert response.result.page == 1
    assert len(response.result.students) == 3
    assert response.result.students[0].student_name == "Charlie"
    assert response.result.students[0].knowledge_classification == "Beginner"
    assert response.result.students[1].student_name == "Diana"
    assert response.result.students[1].knowledge_classification == "Intermediate"
    assert response.result.students[2].student_name == "Eve"
    assert response.result.students[2].knowledge_classification == "Advanced"


@pytest.mark.asyncio
async def test_handler_calls_repository_with_correct_parameters():
    repository = AsyncMock(spec=ReportRepository)
    repository.get_all_students_by_category = AsyncMock(
        return_value=make_paginated_summary()
    )

    handler = GetStudentsByCategoryHandler(repository)
    await handler.handle(
        GetStudentsByCategoryRequest(category="Advanced", page=2, page_size=25)
    )

    repository.get_all_students_by_category.assert_called_once_with(
        category="Advanced", page=2, page_size=25
    )
