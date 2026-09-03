from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_resource_content.get_resource_content_handler import (
    GetResourceContentHandler,
)
from src.features.content_management.get_resource_content.get_resource_content_request import (
    GetResourceRequest,
)
from itmentorsoft_persistence.dto import (
    ContentCategory,
    ResourceContentResponse,
)


@pytest.mark.asyncio
async def test_get_resource_content_when_content_exists_should_return_success():
    content_repository = AsyncMock()
    expected_content = ResourceContentResponse(
        content_id="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
        title="Test Content",
        summary="This is a test content.",
        url="https://example.com/test-content",
        category=ContentCategory.NOVICE,
        related_topics=["Python", "Testing"],
    )
    content_repository.get_resource_content = AsyncMock(return_value=expected_content)

    handler = GetResourceContentHandler(content_repository)

    request = GetResourceRequest(content_id="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Content retrieved successfully"
    assert response.content is not None
    assert response.content.content_id == expected_content.content_id
    assert response.content.title == expected_content.title


@pytest.mark.asyncio
async def test_get_resource_content_when_content_does_not_exist_should_return_failure():
    content_repository = AsyncMock()
    content_repository.get_resource_content = AsyncMock(return_value=None)

    handler = GetResourceContentHandler(content_repository)

    request = GetResourceRequest(content_id="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")
    response = await handler.handle(request)

    assert not response.is_success
    assert response.message == "Content not found"
    assert response.content is None


@pytest.mark.asyncio
async def test_get_resource_content_calls_repository_with_correct_content_id():
    content_repository = AsyncMock()
    content_repository.get_resource_content = AsyncMock(return_value=None)

    handler = GetResourceContentHandler(content_repository)

    request = GetResourceRequest(content_id="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")
    await handler.handle(request)

    content_repository.get_resource_content.assert_called_once_with(
        "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
    )
