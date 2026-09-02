from unittest.mock import AsyncMock
import pytest

from src.features.content_management.update_resource_content.update_resource_content_handler import (
    UpdateResourceContentHandler,
)
from src.features.content_management.update_resource_content.update_resource_content_request import (
    UpdateResourceContentRequest,
)
from itmentorsoft_persistence.dto import ContentCategory

CONTENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def make_request(
    title: str = "Python Basics Guide",
    description: str = "A comprehensive guide to Python programming fundamentals",
    url: str = "https://example.com/python-basics",
    category: str = "principiante",
    related_topic: list[str] | None = None,
) -> UpdateResourceContentRequest:
    return UpdateResourceContentRequest(
        title=title,
        description=description,
        url=url,
        category=category,
        related_topic=related_topic or [],
    )


@pytest.mark.asyncio
async def test_when_update_is_valid_then_should_return_success():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(return_value=None)

    handler = UpdateResourceContentHandler(content_repository)

    request = make_request()
    response = await handler.handle(CONTENT_ID, request)

    assert response.is_success is True
    assert (
        response.message
        == f"Content with ID {CONTENT_ID} has been successfully updated."
    )


@pytest.mark.asyncio
async def test_when_update_is_valid_then_should_call_repository_with_correct_params():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(return_value=None)

    handler = UpdateResourceContentHandler(content_repository)

    request = make_request()
    await handler.handle(CONTENT_ID, request)

    content_repository.update_resource_content.assert_called_once()
    call_args = content_repository.update_resource_content.call_args
    assert call_args[0][0] == CONTENT_ID
    dto = call_args[0][1]
    assert dto.title == request.title
    assert dto.description == request.description
    assert dto.url == request.url
    assert dto.category == request.category
    assert dto.related_topic == request.related_topic


@pytest.mark.asyncio
async def test_when_category_is_empty_then_should_default_to_novice():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(return_value=None)

    handler = UpdateResourceContentHandler(content_repository)

    request = make_request(category="")
    await handler.handle(CONTENT_ID, request)

    assert request.category == ContentCategory.NOVICE.value
    content_repository.update_resource_content.assert_called_once()


@pytest.mark.asyncio
async def test_when_category_is_invalid_then_should_return_failure():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(return_value=None)

    handler = UpdateResourceContentHandler(content_repository)

    request = make_request(category="invalid_category")
    response = await handler.handle(CONTENT_ID, request)

    assert response.is_success is False
    assert response.message == "Invalid category provided"
    content_repository.update_resource_content.assert_not_called()


@pytest.mark.asyncio
async def test_when_related_topic_is_empty_then_should_default_to_empty_list():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(return_value=None)

    handler = UpdateResourceContentHandler(content_repository)

    request = make_request(related_topic=None)
    await handler.handle(CONTENT_ID, request)

    assert request.related_topic == []


@pytest.mark.asyncio
async def test_when_repository_raises_value_error_then_should_return_failure():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(
        side_effect=ValueError("Content not found")
    )

    handler = UpdateResourceContentHandler(content_repository)

    request = make_request()
    response = await handler.handle(CONTENT_ID, request)

    assert response.is_success is False
    assert response.message == "Content not found"


@pytest.mark.asyncio
async def test_when_valid_category_enum_values_then_should_succeed():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(return_value=None)

    handler = UpdateResourceContentHandler(content_repository)

    for category in ContentCategory:
        request = make_request(category=category.value)
        response = await handler.handle(CONTENT_ID, request)
        assert response.is_success is True


@pytest.mark.asyncio
async def test_when_related_topic_has_values_then_should_preserve_them():
    content_repository = AsyncMock()
    content_repository.update_resource_content = AsyncMock(return_value=None)

    handler = UpdateResourceContentHandler(content_repository)

    topics = ["Python", "OOP", "Design Patterns"]
    request = make_request(related_topic=topics)
    await handler.handle(CONTENT_ID, request)

    assert request.related_topic == topics
    content_repository.update_resource_content.assert_called_once()
