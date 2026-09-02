from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_contents_by_topic.get_contents_by_topic_handler import (
    GetContentsByTopicHandler,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_request import (
    GetContentsByTopicPaginationRequest,
)
from itmentorsoft_persistence.dto import (
    ContentCategory,
    PaginatedResourceContentResult,
    ResourceContentResponse,
)


@pytest.mark.asyncio
async def test_get_contents_by_topic_when_repository_returns_items_then_should_return_success():
    content_repository = AsyncMock()
    items = [
        ResourceContentResponse(
            content_id="1",
            title="Test Content",
            summary="A test summary",
            url="https://example.com/test",
            category=ContentCategory.NOVICE,
            related_topics=["Python"],
        )
    ]
    content_repository.get_resource_contents_by_related_topic = AsyncMock(
        return_value=PaginatedResourceContentResult(items=items, total=1)
    )

    handler = GetContentsByTopicHandler(content_repository)
    request = GetContentsByTopicPaginationRequest(topic="Python", page=0, page_size=10)
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Contents retrieved successfully"
    assert len(response.items) == 1
    assert response.total == 1
    content_repository.get_resource_contents_by_related_topic.assert_called_once()
    call_args = content_repository.get_resource_contents_by_related_topic.call_args[0][
        0
    ]
    assert call_args.topic == request.topic
    assert call_args.page == request.page
    assert call_args.page_size == request.page_size


@pytest.mark.asyncio
async def test_get_contents_by_topic_when_repository_returns_empty_then_should_return_empty_list():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_related_topic = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )

    handler = GetContentsByTopicHandler(content_repository)
    request = GetContentsByTopicPaginationRequest(topic="unknown", page=0, page_size=10)
    response = await handler.handle(request)

    assert response.is_success
    assert response.message == "Contents retrieved successfully"
    assert response.items == []
    assert response.total == 0
    content_repository.get_resource_contents_by_related_topic.assert_called_once()
    call_args = content_repository.get_resource_contents_by_related_topic.call_args[0][
        0
    ]
    assert call_args.topic == request.topic
    assert call_args.page == request.page
    assert call_args.page_size == request.page_size


@pytest.mark.asyncio
async def test_get_contents_by_topic_when_custom_pagination_then_should_forward_params():
    content_repository = AsyncMock()
    content_repository.get_resource_contents_by_related_topic = AsyncMock(
        return_value=PaginatedResourceContentResult(items=[], total=0)
    )

    handler = GetContentsByTopicHandler(content_repository)
    request = GetContentsByTopicPaginationRequest(topic="Docker", page=3, page_size=25)
    await handler.handle(request)

    content_repository.get_resource_contents_by_related_topic.assert_called_once()
    call_args = content_repository.get_resource_contents_by_related_topic.call_args[0][
        0
    ]
    assert call_args.topic == request.topic
    assert call_args.page == request.page
    assert call_args.page_size == request.page_size


@pytest.mark.asyncio
async def test_get_contents_by_topic_when_multiple_items_then_should_return_correct_total():
    content_repository = AsyncMock()
    items = [
        ResourceContentResponse(
            content_id=f"id{i}",
            title=f"Content {i}",
            summary="Summary",
            url=f"https://example.com/{i}",
            category=ContentCategory.NOVICE,
            related_topics=[],
        )
        for i in range(5)
    ]
    content_repository.get_resource_contents_by_related_topic = AsyncMock(
        return_value=PaginatedResourceContentResult(items=items, total=50)
    )

    handler = GetContentsByTopicHandler(content_repository)
    request = GetContentsByTopicPaginationRequest(
        topic="Kubernetes", page=0, page_size=5
    )
    response = await handler.handle(request)

    assert response.is_success
    assert len(response.items) == 5
    assert response.total == 50
    content_repository.get_resource_contents_by_related_topic.assert_called_once()
    call_args = content_repository.get_resource_contents_by_related_topic.call_args[0][
        0
    ]
    assert call_args.topic == request.topic
    assert call_args.page == request.page
    assert call_args.page_size == request.page_size
