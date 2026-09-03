from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_learning_path_progress.get_learning_path_progress_handler import (
    GetLearningPathProgressHandler,
)
from src.features.content_management.get_learning_path_progress.get_learning_path_progress_request import (
    GetLearningPathProgressRequest,
)
from itmentorsoft_persistence.dto import (
    LearningPathProgress,
    LearningPathProgressResponse,
)


@pytest.mark.asyncio
async def test_when_repository_returns_success_should_return_progress():
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_progress = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Learning path progress retrieved successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=0.75),
        )
    )

    handler = GetLearningPathProgressHandler(learning_path_repository)
    request = GetLearningPathProgressRequest(path_id="path_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Learning path progress retrieved successfully."
    assert response.path_progress == 0.75
    learning_path_repository.get_learning_path_progress.assert_called_once_with(
        "path_123"
    )


@pytest.mark.asyncio
async def test_when_repository_returns_failure_should_return_error_response():
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_progress = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=False,
            message="Learning path not found.",
            path_progress=None,
        )
    )

    handler = GetLearningPathProgressHandler(learning_path_repository)
    request = GetLearningPathProgressRequest(path_id="invalid_path")
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Learning path not found."
    assert response.path_progress == 0.0
    learning_path_repository.get_learning_path_progress.assert_called_once_with(
        "invalid_path"
    )


@pytest.mark.asyncio
async def test_when_repository_returns_success_with_zero_progress_should_return_zero():
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_progress = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Learning path progress retrieved successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=0.0),
        )
    )

    handler = GetLearningPathProgressHandler(learning_path_repository)
    request = GetLearningPathProgressRequest(path_id="path_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 0.0


@pytest.mark.asyncio
async def test_when_repository_returns_success_without_progress_should_default_to_zero():
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_progress = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Learning path has no progress yet.",
            path_progress=None,
        )
    )

    handler = GetLearningPathProgressHandler(learning_path_repository)
    request = GetLearningPathProgressRequest(path_id="path_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 0.0


@pytest.mark.asyncio
async def test_when_progress_is_complete_should_return_full_progress():
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_progress = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Learning path progress retrieved successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=1.0),
        )
    )

    handler = GetLearningPathProgressHandler(learning_path_repository)
    request = GetLearningPathProgressRequest(path_id="path_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 1.0
    assert response.message == "Learning path progress retrieved successfully."


@pytest.mark.asyncio
async def test_when_repository_raises_exception_should_propagate():
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_progress = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = GetLearningPathProgressHandler(learning_path_repository)
    request = GetLearningPathProgressRequest(path_id="path_123")

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(request)


@pytest.mark.asyncio
async def test_when_progress_is_halfway_should_return_correct_value():
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_progress = AsyncMock(
        return_value=LearningPathProgressResponse(
            is_success=True,
            message="Learning path progress retrieved successfully.",
            path_progress=LearningPathProgress(path_id="path_123", progress=0.5),
        )
    )

    handler = GetLearningPathProgressHandler(learning_path_repository)
    request = GetLearningPathProgressRequest(path_id="path_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.path_progress == 0.5
