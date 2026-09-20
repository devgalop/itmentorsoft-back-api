from unittest.mock import AsyncMock
import pytest

from src.features.content_management.update_rating.update_rating_handler import (
    UpdateRatingHandler,
)
from src.features.content_management.update_rating.update_rating_request import (
    UpdateRatingRequest,
)
from src.features.content_management.update_rating.update_rating_response import (
    UpdateRatingResponse,
)
from itmentorsoft_persistence.dto import RateContent


@pytest.mark.asyncio
async def test_update_rating_when_rating_exists_then_should_update_successfully():
    content_repository = AsyncMock()
    content_repository.get_rating_content_by_user = AsyncMock(return_value=True)
    content_repository.update_rating = AsyncMock()

    handler = UpdateRatingHandler(content_repository)

    request = UpdateRatingRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=4,
        comment="Great content!",
    )
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Rating updated successfully"
    content_repository.get_rating_content_by_user.assert_called_once_with(
        "valid_user_id_456", "valid_content_id_123"
    )
    content_repository.update_rating.assert_called_once()


@pytest.mark.asyncio
async def test_update_rating_when_rating_not_found_then_should_return_failure():
    content_repository = AsyncMock()
    content_repository.get_rating_content_by_user = AsyncMock(return_value=None)

    handler = UpdateRatingHandler(content_repository)

    request = UpdateRatingRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=4,
    )
    response = await handler.handle(request)

    assert not response.is_success
    assert response.message == "Rating not found"
    content_repository.get_rating_content_by_user.assert_called_once_with(
        "valid_user_id_456", "valid_content_id_123"
    )
    content_repository.update_rating.assert_not_called()


@pytest.mark.asyncio
async def test_update_rating_when_request_is_valid_should_call_update_rating_repository():
    content_repository = AsyncMock()
    content_repository.get_rating_content_by_user = AsyncMock(return_value=True)
    content_repository.update_rating = AsyncMock()

    handler = UpdateRatingHandler(content_repository)

    request = UpdateRatingRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=5,
        comment="Excellent!",
    )
    await handler.handle(request)

    content_repository.update_rating.assert_called_once()
    call_args = content_repository.update_rating.call_args
    rated_content = call_args[0][0]
    assert isinstance(rated_content, RateContent)
    assert rated_content.user_id == "valid_user_id_456"
    assert rated_content.content_id == "valid_content_id_123"
    assert rated_content.rating == 5
    assert rated_content.comment == "Excellent!"


@pytest.mark.asyncio
async def test_update_rating_when_rating_exists_should_return_success_response():
    content_repository = AsyncMock()
    content_repository.get_rating_content_by_user = AsyncMock(return_value=True)
    content_repository.update_rating = AsyncMock()

    handler = UpdateRatingHandler(content_repository)

    request = UpdateRatingRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=3,
    )
    response = await handler.handle(request)

    assert response.is_success
    assert isinstance(response, UpdateRatingResponse)
    content_repository.get_rating_content_by_user.assert_called_once()
    content_repository.update_rating.assert_called_once()


@pytest.mark.asyncio
async def test_update_rating_should_pass_correct_rate_content_fields():
    content_repository = AsyncMock()
    content_repository.get_rating_content_by_user = AsyncMock(return_value=True)
    content_repository.update_rating = AsyncMock()

    handler = UpdateRatingHandler(content_repository)

    request = UpdateRatingRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=4,
        comment="Good!",
    )
    await handler.handle(request)

    call_args = content_repository.update_rating.call_args
    rated_content = call_args[0][0]
    assert rated_content.user_id == "valid_user_id_456"
    assert rated_content.content_id == "valid_content_id_123"
    assert rated_content.rating == 4
    assert rated_content.comment == "Good!"
