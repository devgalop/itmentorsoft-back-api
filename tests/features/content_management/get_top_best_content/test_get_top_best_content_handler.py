from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_top_best_content.get_top_best_content_handler import (
    GetTopBestContentHandler,
)
from src.features.content_management.get_top_best_content.get_top_best_content_request import (
    GetTopBestContentRequest,
)
from itmentorsoft_persistence.dto import ResourceContentRating


@pytest.mark.asyncio
async def test_when_content_exists_should_return_top_best_content():
    content_repository = AsyncMock()
    content_repository.get_top_content = AsyncMock(
        return_value=[
            ResourceContentRating(
                content_id="id_1",
                title="Best Python Guide",
                summary="A great Python tutorial",
                rating=4.9,
            ),
            ResourceContentRating(
                content_id="id_2",
                title="Advanced Python",
                summary="Deep dive into Python",
                rating=4.7,
            ),
        ]
    )

    handler = GetTopBestContentHandler(content_repository)
    response = await handler.handle(GetTopBestContentRequest(topic="python", limit=5))

    assert response.is_success is True
    assert response.message == "Top best content retrieved successfully."
    assert len(response.items) == 2
    assert response.items[0].content_id == "id_1"
    assert response.items[0].rating == 4.9
    assert response.items[1].content_id == "id_2"
    content_repository.get_top_content.assert_called_once_with(
        topic="python", limit=5, order="desc"
    )


@pytest.mark.asyncio
async def test_when_no_content_found_should_return_failure_response():
    content_repository = AsyncMock()
    content_repository.get_top_content = AsyncMock(return_value=[])

    handler = GetTopBestContentHandler(content_repository)
    response = await handler.handle(
        GetTopBestContentRequest(topic="unknown_topic", limit=10)
    )

    assert response.is_success is False
    assert response.message == "No top best content found for the given topic."
    assert response.items == []
    content_repository.get_top_content.assert_called_once_with(
        topic="unknown_topic", limit=10, order="desc"
    )


@pytest.mark.asyncio
async def test_when_content_exists_should_map_all_fields_correctly():
    content_repository = AsyncMock()
    content_repository.get_top_content = AsyncMock(
        return_value=[
            ResourceContentRating(
                content_id="abc123",
                title="Test Title",
                summary="Test Summary",
                rating=3.5,
            ),
        ]
    )

    handler = GetTopBestContentHandler(content_repository)
    response = await handler.handle(GetTopBestContentRequest(topic="testing", limit=1))

    assert response.items[0].content_id == "abc123"
    assert response.items[0].title == "Test Title"
    assert response.items[0].summary == "Test Summary"
    assert response.items[0].rating == 3.5
