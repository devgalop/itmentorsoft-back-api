from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_top_worse_content.get_top_worse_content_handler import (
    GetTopWorseContentHandler,
)
from src.features.content_management.get_top_worse_content.get_top_worse_content_request import (
    GetTopWorseContentRequest,
)
from itmentorsoft_persistence.dto import ResourceContentRating


@pytest.mark.asyncio
async def test_when_content_exists_should_return_top_worse_content():
    content_repository = AsyncMock()
    content_repository.get_top_content = AsyncMock(
        return_value=[
            ResourceContentRating(
                content_id="id_1",
                title="Poor Python Guide",
                summary="A confusing tutorial",
                rating=1.2,
            ),
            ResourceContentRating(
                content_id="id_2",
                title="Bad Python Tips",
                summary="Outdated information",
                rating=1.5,
            ),
        ]
    )

    handler = GetTopWorseContentHandler(content_repository)
    response = await handler.handle(GetTopWorseContentRequest(topic="python", limit=5))

    assert response.is_success is True
    assert response.message == "Top worse content retrieved successfully."
    assert len(response.items) == 2
    assert response.items[0].content_id == "id_1"
    assert response.items[0].rating == 1.2
    assert response.items[1].content_id == "id_2"
    content_repository.get_top_content.assert_called_once_with(
        topic="python", limit=5, order="asc"
    )


@pytest.mark.asyncio
async def test_when_no_content_found_should_return_failure_response():
    content_repository = AsyncMock()
    content_repository.get_top_content = AsyncMock(return_value=[])

    handler = GetTopWorseContentHandler(content_repository)
    response = await handler.handle(
        GetTopWorseContentRequest(topic="unknown_topic", limit=10)
    )

    assert response.is_success is False
    assert response.message == "No top worse content found for the given topic."
    assert response.items == []
    content_repository.get_top_content.assert_called_once_with(
        topic="unknown_topic", limit=10, order="asc"
    )


@pytest.mark.asyncio
async def test_when_content_exists_should_map_all_fields_correctly():
    content_repository = AsyncMock()
    content_repository.get_top_content = AsyncMock(
        return_value=[
            ResourceContentRating(
                content_id="xyz789",
                title="Worst Title",
                summary="Worst Summary",
                rating=0.5,
            ),
        ]
    )

    handler = GetTopWorseContentHandler(content_repository)
    response = await handler.handle(GetTopWorseContentRequest(topic="testing", limit=1))

    assert response.items[0].content_id == "xyz789"
    assert response.items[0].title == "Worst Title"
    assert response.items[0].summary == "Worst Summary"
    assert response.items[0].rating == 0.5
