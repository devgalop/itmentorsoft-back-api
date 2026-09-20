from unittest.mock import AsyncMock, MagicMock
import pytest
from src.features.content_management.get_rating_by_user.get_rating_by_user_handler import (
    GetContentRatingByUserHandler,
)
from src.features.content_management.get_rating_by_user.get_rating_by_user_request import (
    GetContentRatingByUserRequest,
)


@pytest.mark.asyncio
async def test_when_ratings_exist_then_should_return_success_with_ratings():
    content_repository = AsyncMock()
    mock_rating = MagicMock()
    mock_rating.content_id = "valid_content_id_123"
    mock_rating.title = "Test Title"
    mock_rating.summary = "Test Summary"
    mock_rating.rating = 4.5
    mock_rating.student_id = "valid_student_id_1"
    content_repository.get_ratings_by_user = AsyncMock(return_value=[mock_rating])
    handler = GetContentRatingByUserHandler(content_repository)
    request = GetContentRatingByUserRequest(user_id="valid_user_id_456")
    response = await handler.handle(request)
    assert response.is_success
    assert response.message == "Ratings retrieved successfully."
    assert len(response.rating_details) == 1
    content_repository.get_ratings_by_user.assert_called_once_with("valid_user_id_456")


@pytest.mark.asyncio
async def test_when_no_ratings_found_then_should_return_failure_with_empty_list():
    content_repository = AsyncMock()
    content_repository.get_ratings_by_user = AsyncMock(return_value=[])
    handler = GetContentRatingByUserHandler(content_repository)
    request = GetContentRatingByUserRequest(user_id="valid_user_id_456")
    response = await handler.handle(request)
    assert not response.is_success
    assert response.message == "No ratings found for the user."
    assert response.rating_details == []
    content_repository.get_ratings_by_user.assert_called_once_with("valid_user_id_456")


@pytest.mark.asyncio
async def test_when_repository_returns_ratings_then_should_map_fields_correctly():
    content_repository = AsyncMock()
    mock_rating = MagicMock()
    mock_rating.content_id = "content_abc123"
    mock_rating.title = "Mapped Title"
    mock_rating.summary = "Mapped Summary"
    mock_rating.rating = 3.7
    mock_rating.student_id = "student_xyz789"
    content_repository.get_ratings_by_user = AsyncMock(return_value=[mock_rating])
    handler = GetContentRatingByUserHandler(content_repository)
    request = GetContentRatingByUserRequest(user_id="valid_user_id_456")
    response = await handler.handle(request)
    assert response.is_success
    assert len(response.rating_details) == 1
    detail = response.rating_details[0]
    assert detail.content_id == "content_abc123"
    assert detail.title == "Mapped Title"
    assert detail.summary == "Mapped Summary"
    assert detail.rating == 3.7
    assert detail.student_id == "student_xyz789"
    content_repository.get_ratings_by_user.assert_called_once_with("valid_user_id_456")


@pytest.mark.asyncio
async def test_when_multiple_ratings_then_should_return_all_ratings():
    content_repository = AsyncMock()
    mock_rating_1 = MagicMock()
    mock_rating_1.content_id = "content_one_001"
    mock_rating_1.title = "First Content"
    mock_rating_1.summary = "First Summary"
    mock_rating_1.rating = 5.0
    mock_rating_1.student_id = "student_001"
    mock_rating_2 = MagicMock()
    mock_rating_2.content_id = "content_two_002"
    mock_rating_2.title = "Second Content"
    mock_rating_2.summary = "Second Summary"
    mock_rating_2.rating = 2.5
    mock_rating_2.student_id = "student_002"
    content_repository.get_ratings_by_user = AsyncMock(
        return_value=[mock_rating_1, mock_rating_2]
    )
    handler = GetContentRatingByUserHandler(content_repository)
    request = GetContentRatingByUserRequest(user_id="valid_user_id_456")
    response = await handler.handle(request)
    assert response.is_success
    assert response.message == "Ratings retrieved successfully."
    assert len(response.rating_details) == 2
    assert response.rating_details[0].content_id == "content_one_001"
    assert response.rating_details[0].rating == 5.0
    assert response.rating_details[1].content_id == "content_two_002"
    assert response.rating_details[1].rating == 2.5
    content_repository.get_ratings_by_user.assert_called_once_with("valid_user_id_456")
