from unittest.mock import AsyncMock
import pytest

from src.features.content_management.rate_content.rate_content_handler import (
    RateContentHandler,
)
from src.features.content_management.rate_content.rate_content_request import (
    RateContentRequest,
)
from src.features.content_management.rate_content.rate_content_response import (
    RateContentResponse,
)
from itmentorsoft_persistence.dto import RateContent
from itmentorsoft_persistence.dto import (
    ResourceContent,
)


@pytest.mark.asyncio
async def test_rate_content_when_content_exists_then_should_rate_content_successfully():
    content_repository = AsyncMock()
    content_repository.get_resource_content = AsyncMock(return_value=ResourceContent())
    content_repository.rate_resource_content = AsyncMock()

    handler = RateContentHandler(content_repository)

    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=4,
        comment="Great content!",
    )
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Content rated successfully."
    content_repository.get_resource_content.assert_called_once_with(
        "valid_content_id_123"
    )
    content_repository.rate_resource_content.assert_called_once()


@pytest.mark.asyncio
async def test_rate_content_when_content_not_found_then_should_return_failure():
    content_repository = AsyncMock()
    content_repository.get_resource_content = AsyncMock(return_value=None)

    handler = RateContentHandler(content_repository)

    request = RateContentRequest(
        content_id="nonexistent_content_id",
        user_id="valid_user_id_456",
        rating=4,
    )
    response = await handler.handle(request)

    assert not response.is_success
    assert response.message == "Content with ID nonexistent_content_id not found."
    content_repository.get_resource_content.assert_called_once_with(
        "nonexistent_content_id"
    )
    content_repository.rate_resource_content.assert_not_called()


@pytest.mark.asyncio
async def test_rate_content_when_request_is_valid_should_call_rate_repository():
    content_repository = AsyncMock()
    content_repository.get_resource_content = AsyncMock(return_value=ResourceContent())
    content_repository.rate_resource_content = AsyncMock()

    handler = RateContentHandler(content_repository)

    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=5,
        comment="Excellent!",
    )
    await handler.handle(request)

    content_repository.rate_resource_content.assert_called_once()
    call_args = content_repository.rate_resource_content.call_args
    rated_content = call_args[0][0]
    assert isinstance(rated_content, RateContent)
    assert rated_content.content_id == "valid_content_id_123"
    assert rated_content.user_id == "valid_user_id_456"
    assert rated_content.rating == 5
    assert rated_content.comment == "Excellent!"


@pytest.mark.asyncio
async def test_rate_content_when_rating_is_valid_should_return_success_response():
    content_repository = AsyncMock()
    content_repository.get_resource_content = AsyncMock(return_value=ResourceContent())
    content_repository.rate_resource_content = AsyncMock()

    handler = RateContentHandler(content_repository)

    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=3,
    )
    response = await handler.handle(request)

    assert response.is_success
    assert isinstance(response, RateContentResponse)
    content_repository.get_resource_content.assert_called_once()
    content_repository.rate_resource_content.assert_called_once()


@pytest.mark.asyncio
async def test_rate_content_should_use_uuid_for_rating_id():
    content_repository = AsyncMock()
    content_repository.get_resource_content = AsyncMock(return_value=ResourceContent())
    content_repository.rate_resource_content = AsyncMock()

    handler = RateContentHandler(content_repository)

    request = RateContentRequest(
        content_id="valid_content_id_123",
        user_id="valid_user_id_456",
        rating=4,
    )
    await handler.handle(request)

    call_args = content_repository.rate_resource_content.call_args
    rated_content = call_args[0][0]
    assert rated_content.id is not None
    assert len(rated_content.id) > 0
