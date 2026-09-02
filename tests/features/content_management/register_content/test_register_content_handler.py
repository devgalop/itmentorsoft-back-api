from unittest.mock import AsyncMock
import pytest

from src.features.content_management.register_content.register_content_handler import (
    RegisterContentHandler,
)
from src.features.content_management.register_content.register_content_request import (
    RegisterContentRequest,
)
from itmentorsoft_persistence.dto import (
    ContentCategory,
    PaginatedResourceContentResult,
    ResourceContent,
    ResourceContentBuilder,
)


@pytest.mark.asyncio
async def test_register_content_when_is_valid_then_should_register_content_successfully():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_title = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )
    content_repository.save = AsyncMock()

    handler = RegisterContentHandler(content_repository, ResourceContentBuilder)

    request = RegisterContentRequest(
        title="Test Content",
        description="This is a test content.",
        url="https://example.com/test-content",
        category="principiante",
        related_topic=["Python", "Testing"],
    )
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Content registered successfully"
    content_repository.get_resource_contents_by_title.assert_called_once()
    content_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_content_when_title_already_exists_should_return_failure():
    content_repository = AsyncMock()
    existing_content = ResourceContent()
    existing_content.add_title("Test Content")
    content_repository.get_resource_contents_by_title = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[existing_content], total=1)
    )

    handler = RegisterContentHandler(content_repository, ResourceContentBuilder)

    request = RegisterContentRequest(
        title="Test Content",
        description="This is a test content.",
        url="https://example.com/test-content",
        category="principiante",
        related_topic=["Python"],
    )
    response = await handler.handle(request)

    assert not response.is_success
    assert response.content_id is None
    assert response.message == "Content with the same title already exists"
    content_repository.get_resource_contents_by_title.assert_called_once()
    content_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_content_when_category_is_invalid_should_return_failure():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_title = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )

    handler = RegisterContentHandler(content_repository, ResourceContentBuilder)

    request = RegisterContentRequest(
        title="Test Content",
        description="This is a test content.",
        url="https://example.com/test-content",
        category="invalid_category",
        related_topic=["Python"],
    )
    response = await handler.handle(request)

    assert not response.is_success
    assert response.content_id is None
    assert response.message == "Invalid category provided"
    content_repository.get_resource_contents_by_title.assert_called_once()
    content_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_register_content_when_category_is_not_provided_should_use_default_novice():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_title = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )
    content_repository.save = AsyncMock()

    handler = RegisterContentHandler(content_repository, ResourceContentBuilder)

    request = RegisterContentRequest(
        title="Test Content",
        description="This is a test content.",
        url="https://example.com/test-content",
        category="principiante",
        related_topic=[],
    )
    await handler.handle(request)

    call_args = content_repository.save.call_args
    saved_content = call_args[0][0]
    assert saved_content.category == ContentCategory.NOVICE
    content_repository.get_resource_contents_by_title.assert_called_once()
    content_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_content_when_related_topic_is_not_provided_should_use_default_empty_list():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_title = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )
    content_repository.save = AsyncMock()

    handler = RegisterContentHandler(content_repository, ResourceContentBuilder)

    request = RegisterContentRequest(
        title="Test Content",
        description="This is a test content.",
        url="https://example.com/test-content",
        category="principiante",
        related_topic=[],
    )
    await handler.handle(request)

    call_args = content_repository.save.call_args
    saved_content = call_args[0][0]
    assert saved_content.related_topics == []
    content_repository.get_resource_contents_by_title.assert_called_once()
    content_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_content_when_request_is_valid_should_return_content_id():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_title = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )
    content_repository.save = AsyncMock()

    handler = RegisterContentHandler(content_repository, ResourceContentBuilder)

    request = RegisterContentRequest(
        title="Test Content",
        description="This is a test content.",
        url="https://example.com/test-content",
        category="principiante",
        related_topic=["Python"],
    )
    response = await handler.handle(request)

    assert response.is_success
    assert response.content_id is not None
    assert isinstance(response.content_id, str)
    assert response.message == "Content registered successfully"
    content_repository.get_resource_contents_by_title.assert_called_once()
    content_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_register_content_when_category_is_empty_string_then_defaults_to_novice():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_title = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )
    content_repository.save = AsyncMock()

    handler = RegisterContentHandler(content_repository, ResourceContentBuilder)

    request = RegisterContentRequest(
        title="Test Content",
        description="This is a test content.",
        url="https://example.com/test-content",
        category="principiante",
        related_topic=[],
    )
    request.category = ""  # force empty to trigger default branch

    response = await handler.handle(request)

    assert response.is_success
    call_args = content_repository.save.call_args
    saved_content = call_args[0][0]
    assert saved_content.category == ContentCategory.NOVICE
