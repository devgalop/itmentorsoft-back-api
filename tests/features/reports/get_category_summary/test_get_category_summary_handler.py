from unittest.mock import AsyncMock
import pytest

from src.features.reports.get_category_summary.get_category_summary_handler import (
    GetCategorySummaryHandler,
)
from src.features.reports.get_category_summary.get_category_summary_request import (
    GetCategorySummaryRequest,
)
from src.features.reports.get_category_summary.get_category_summary_response import (
    GetCategorySummaryResponse,
)
from itmentorsoft_persistence.dto import (
    CategorySummary as DomainCategorySummary,
)
from src.features.reports.shared.student_report_service import (
    GetCategorySummary,
    StudentReportService,
)


@pytest.mark.asyncio
async def test_when_category_exists_then_return_success_with_summary():
    service = AsyncMock(spec=StudentReportService)
    service.get_category_summary = AsyncMock(
        return_value=GetCategorySummary(
            is_success=True,
            message="Category summary retrieved successfully",
            category_summary=DomainCategorySummary(
                category="Mathematics", total_students=150
            ),
        )
    )

    handler = GetCategorySummaryHandler(service)
    response = await handler.handle(GetCategorySummaryRequest(category="Mathematics"))

    assert isinstance(response, GetCategorySummaryResponse)
    assert response.is_success is True
    assert response.message == "Category summary retrieved successfully"
    assert response.category_summary is not None
    assert response.category_summary.category == "Mathematics"
    assert response.category_summary.total_students == 150


@pytest.mark.asyncio
async def test_when_service_returns_failure_then_return_failure():
    service = AsyncMock(spec=StudentReportService)
    service.get_category_summary = AsyncMock(
        return_value=GetCategorySummary(
            is_success=False,
            message="Category summary not found",
            category_summary=None,
        )
    )

    handler = GetCategorySummaryHandler(service)
    response = await handler.handle(GetCategorySummaryRequest(category="Nonexistent"))

    assert isinstance(response, GetCategorySummaryResponse)
    assert response.is_success is False
    assert response.message == "Category summary not found"


@pytest.mark.asyncio
async def test_when_service_returns_success_but_no_summary_then_return_failure():
    service = AsyncMock(spec=StudentReportService)
    service.get_category_summary = AsyncMock(
        return_value=GetCategorySummary(
            is_success=True,
            message="Category summary retrieved successfully",
            category_summary=None,
        )
    )

    handler = GetCategorySummaryHandler(service)
    response = await handler.handle(GetCategorySummaryRequest(category="Mathematics"))

    assert isinstance(response, GetCategorySummaryResponse)
    assert response.is_success is False
    assert response.category_summary.category == ""
    assert response.category_summary.total_students == 0


@pytest.mark.asyncio
async def test_map_to_response_converts_category_summary_correctly():
    service = AsyncMock(spec=StudentReportService)
    service.get_category_summary = AsyncMock(
        return_value=GetCategorySummary(
            is_success=True,
            message="Category summary retrieved successfully",
            category_summary=DomainCategorySummary(
                category="Science", total_students=75
            ),
        )
    )

    handler = GetCategorySummaryHandler(service)
    response = await handler.handle(GetCategorySummaryRequest(category="Science"))

    assert response.category_summary.category == "Science"
    assert response.category_summary.total_students == 75


@pytest.mark.asyncio
async def test_handler_calls_service_with_correct_category():
    service = AsyncMock(spec=StudentReportService)
    service.get_category_summary = AsyncMock(
        return_value=GetCategorySummary(
            is_success=True,
            message="Category summary retrieved successfully",
            category_summary=DomainCategorySummary(
                category="History", total_students=50
            ),
        )
    )

    handler = GetCategorySummaryHandler(service)
    await handler.handle(GetCategorySummaryRequest(category="History"))

    service.get_category_summary.assert_called_once_with("History")
