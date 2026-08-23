from unittest.mock import AsyncMock
import pytest

from src.features.content_management.update_content_path_status.update_content_path_status_handler import (
    UpdateContentPathStatusHandler,
)
from src.features.content_management.update_content_path_status.update_content_path_status_request import (
    UpdateContentPathStatusRequest,
)
from src.features.content_management.shared.learning_path import (
    LearningPathProgress,
    LearningPathProgressResponse,
)


@pytest.mark.asyncio
async def test_when_repository_returns_success_should_return_response_with_progress():
    learning_path_repository = AsyncMock()
    learning_path_repository.update_status_content_path = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Content path status updated successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=0.75),
        )
    )

    handler = UpdateContentPathStatusHandler(learning_path_repository)
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=True
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Content path status updated successfully."
    assert response.path_progress == 0.75
    learning_path_repository.update_status_content_path.assert_called_once_with(
        "path_123", "content_456", True
    )


@pytest.mark.asyncio
async def test_when_repository_returns_failure_should_return_error_response():
    learning_path_repository = AsyncMock()
    learning_path_repository.update_status_content_path = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=False,
            message="Content path not found.",
            path_progress=None,
        )
    )

    handler = UpdateContentPathStatusHandler(learning_path_repository)
    request = UpdateContentPathStatusRequest(
        path_id="invalid_path", content_id="content_456", status=True
    )
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Content path not found."
    assert response.path_progress == 0.0
    learning_path_repository.update_status_content_path.assert_called_once_with(
        "invalid_path", "content_456", True
    )


@pytest.mark.asyncio
async def test_when_repository_returns_success_with_zero_progress_should_return_zero():
    learning_path_repository = AsyncMock()
    learning_path_repository.update_status_content_path = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Content path status updated successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=0.0),
        )
    )

    handler = UpdateContentPathStatusHandler(learning_path_repository)
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=False
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 0.0


@pytest.mark.asyncio
async def test_when_repository_returns_success_without_progress_should_default_to_zero():
    learning_path_repository = AsyncMock()
    learning_path_repository.update_status_content_path = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Content path status updated.",
            path_progress=None,
        )
    )

    handler = UpdateContentPathStatusHandler(learning_path_repository)
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=True
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 0.0


@pytest.mark.asyncio
async def test_when_status_is_false_should_return_success_with_progress():
    learning_path_repository = AsyncMock()
    learning_path_repository.update_status_content_path = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Content path status updated successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=0.5),
        )
    )

    handler = UpdateContentPathStatusHandler(learning_path_repository)
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=False
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 0.5
    learning_path_repository.update_status_content_path.assert_called_once_with(
        "path_123", "content_456", False
    )


@pytest.mark.asyncio
async def test_when_repository_raises_exception_should_propagate():
    learning_path_repository = AsyncMock()
    learning_path_repository.update_status_content_path = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = UpdateContentPathStatusHandler(learning_path_repository)
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=True
    )

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(request)


@pytest.mark.asyncio
async def test_when_progress_is_complete_should_return_full_progress():
    learning_path_repository = AsyncMock()
    learning_path_repository.update_status_content_path = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Content path status updated successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=1.0),
        )
    )

    handler = UpdateContentPathStatusHandler(learning_path_repository)
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=True
    )
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 1.0
    assert response.message == "Content path status updated successfully."
