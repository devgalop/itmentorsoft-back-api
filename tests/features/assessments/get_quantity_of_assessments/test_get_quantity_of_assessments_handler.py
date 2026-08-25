from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_quantity_of_assessments.get_quantity_of_assessments_handler import (
    GetQuantityOfAssessmentsHandler,
)
from src.features.assessments.get_quantity_of_assessments.get_quantity_of_assessments_request import (
    GetQuantityOfAssessmentsRequest,
)


@pytest.mark.asyncio
async def test_when_student_has_assessments_should_return_total_count():
    assessment_repository = AsyncMock()
    assessment_repository.get_quantity_of_assessments = AsyncMock(return_value=5)

    handler = GetQuantityOfAssessmentsHandler(assessment_repository)
    response = await handler.handle(
        GetQuantityOfAssessmentsRequest(student_id="student_123")
    )

    assert response.is_success is True
    assert response.message == "Quantity of assessments retrieved successfully."
    assert response.total_assessments == 5
    assessment_repository.get_quantity_of_assessments.assert_called_once_with(
        "student_123"
    )


@pytest.mark.asyncio
async def test_when_student_has_no_assessments_should_return_zero():
    assessment_repository = AsyncMock()
    assessment_repository.get_quantity_of_assessments = AsyncMock(return_value=0)

    handler = GetQuantityOfAssessmentsHandler(assessment_repository)
    response = await handler.handle(
        GetQuantityOfAssessmentsRequest(student_id="student_456")
    )

    assert response.is_success is True
    assert response.message == "Quantity of assessments retrieved successfully."
    assert response.total_assessments == 0
    assessment_repository.get_quantity_of_assessments.assert_called_once_with(
        "student_456"
    )


@pytest.mark.asyncio
async def test_when_repository_raises_error_should_propagate_exception():
    assessment_repository = AsyncMock()
    assessment_repository.get_quantity_of_assessments = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = GetQuantityOfAssessmentsHandler(assessment_repository)

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(GetQuantityOfAssessmentsRequest(student_id="student_789"))

    assessment_repository.get_quantity_of_assessments.assert_called_once_with(
        "student_789"
    )
