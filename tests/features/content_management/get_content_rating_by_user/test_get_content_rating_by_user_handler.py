from unittest.mock import AsyncMock, MagicMock
import pytest
from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_handler import (
    GetContentRatingByUserHandler,
)
from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_request import (
    GetContentRatingByUserRequest,
)


@pytest.mark.asyncio
async def test_when_rating_exists_then_should_return_success_with_rating_detail():
    content_repository = AsyncMock()
    mock_rating = MagicMock()
    mock_rating.content_id = "valid_content_id_123"
    mock_rating.title = "Test Title"
    mock_rating.summary = "Test Summary"
    mock_rating.rating = 4.5
    mock_rating.student_id = "valid_student_id_1"
    content_repository.get_rating_content_by_user = AsyncMock(return_value=mock_rating)
    handler = GetContentRatingByUserHandler(content_repository)
    request = GetContentRatingByUserRequest(
        user_id="valid_user_id_456", content_id="valid_content_id_123"
    )
    response = await handler.handle(request)
    assert response.is_success
    assert response.message == "Rating retrieved successfully"
    assert response.rating_detail is not None
    content_repository.get_rating_content_by_user.assert_called_once_with(
        "valid_user_id_456", "valid_content_id_123"
    )


@pytest.mark.asyncio
async def test_when_rating_not_found_then_should_return_failure_with_none():
    content_repository = AsyncMock()
    content_repository.get_rating_content_by_user = AsyncMock(return_value=None)
    handler = GetContentRatingByUserHandler(content_repository)
    request = GetContentRatingByUserRequest(
        user_id="valid_user_id_456", content_id="valid_content_id_123"
    )
    response = await handler.handle(request)
    assert not response.is_success
    assert response.message == "Rating not found"
    assert response.rating_detail is None
    content_repository.get_rating_content_by_user.assert_called_once_with(
        "valid_user_id_456", "valid_content_id_123"
    )


@pytest.mark.asyncio
async def test_when_rating_found_then_should_map_fields_correctly():
    content_repository = AsyncMock()
    mock_rating = MagicMock()
    mock_rating.content_id = "content_abc123"
    mock_rating.title = "Mapped Title"
    mock_rating.summary = "Mapped Summary"
    mock_rating.rating = 3.7
    mock_rating.student_id = "student_xyz789"
    content_repository.get_rating_content_by_user = AsyncMock(return_value=mock_rating)
    handler = GetContentRatingByUserHandler(content_repository)
    request = GetContentRatingByUserRequest(
        user_id="valid_user_id_456", content_id="valid_content_id_123"
    )
    response = await handler.handle(request)
    assert response.is_success
    assert response.rating_detail is not None
    detail = response.rating_detail
    assert detail.content_id == "content_abc123"
    assert detail.title == "Mapped Title"
    assert detail.summary == "Mapped Summary"
    assert detail.rating == 3.7
    assert detail.student_id == "student_xyz789"
    content_repository.get_rating_content_by_user.assert_called_once_with(
        "valid_user_id_456", "valid_content_id_123"
    )
