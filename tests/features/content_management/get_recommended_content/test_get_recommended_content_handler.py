from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_recommended_content.get_recommended_content_handler import (
    GetRecommendedContentHandler,
)
from src.features.content_management.get_recommended_content.get_recommended_content_request import (
    GetRecommendedContentRequest,
)
from itmentorsoft_persistence.dto import (
    ContentByTopic,
    LearningPath,
    LearningPathResponse,
)


@pytest.mark.asyncio
async def test_when_repository_returns_success_should_return_mapped_recommendations():
    learning_path_repository = AsyncMock()

    content = ContentByTopic(
        content_id="content_1",
        title="Intro to Python",
        description="Learn Python basics",
        rating=4.5,
    )
    learning_path = LearningPath(
        path_id="path_1",
        user_id="student_123",
        topic="Python",
        is_completed=False,
        contents=[content],
    )
    learning_path_repository.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=True,
            message="Paths found",
            recommendation=[learning_path],
        )
    )
    learning_path_repository.save_learning_path = AsyncMock()

    handler = GetRecommendedContentHandler(learning_path_repository)
    response = await handler.handle(
        GetRecommendedContentRequest(student_id="student_123")
    )

    assert response.is_success is True
    assert response.message == "Learning paths retrieved successfully."
    assert len(response.recommendation) == 1
    assert response.recommendation[0].topic == "Python"
    assert len(response.recommendation[0].contents) == 1
    assert response.recommendation[0].contents[0].content_id == "content_1"
    assert response.recommendation[0].contents[0].title == "Intro to Python"
    assert response.recommendation[0].contents[0].rating == 4.5
    learning_path_repository.get_learning_path.assert_called_once_with("student_123")
    learning_path_repository.save_learning_path.assert_called_once_with(learning_path)


@pytest.mark.asyncio
async def test_when_repository_returns_failure_should_return_failure_response():
    learning_path_repository = AsyncMock()

    learning_path_repository.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=False,
            message="Repository error",
            recommendation=[],
        )
    )

    handler = GetRecommendedContentHandler(learning_path_repository)
    response = await handler.handle(
        GetRecommendedContentRequest(student_id="student_123")
    )

    assert response.is_success is False
    assert response.message == "Failed to retrieve learning paths."
    assert response.recommendation == []
    learning_path_repository.get_learning_path.assert_called_once_with("student_123")
    learning_path_repository.save_learning_path.assert_not_called()


@pytest.mark.asyncio
async def test_when_repository_returns_empty_recommendations_should_return_empty_list():
    learning_path_repository = AsyncMock()

    learning_path_repository.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=True,
            message="No paths",
            recommendation=[],
        )
    )

    handler = GetRecommendedContentHandler(learning_path_repository)
    response = await handler.handle(
        GetRecommendedContentRequest(student_id="student_123")
    )

    assert response.is_success is True
    assert response.message == "Learning paths retrieved successfully."
    assert response.recommendation == []
    learning_path_repository.get_learning_path.assert_called_once_with("student_123")
    learning_path_repository.save_learning_path.assert_not_called()


@pytest.mark.asyncio
async def test_when_multiple_learning_paths_should_save_all_and_map_correctly():
    learning_path_repository = AsyncMock()

    content_1 = ContentByTopic("c1", "Title 1", "Desc 1", 3.0)
    content_2 = ContentByTopic("c2", "Title 2", "Desc 2", 4.0)
    path_1 = LearningPath("p1", "student_123", "Math", False, [content_1])
    path_2 = LearningPath("p2", "student_123", "Science", True, [content_2])

    learning_path_repository.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=True,
            message="Found",
            recommendation=[path_1, path_2],
        )
    )
    learning_path_repository.save_learning_path = AsyncMock()

    handler = GetRecommendedContentHandler(learning_path_repository)
    response = await handler.handle(
        GetRecommendedContentRequest(student_id="student_123")
    )

    assert response.is_success is True
    assert len(response.recommendation) == 2
    assert response.recommendation[0].topic == "Math"
    assert response.recommendation[1].topic == "Science"
    assert learning_path_repository.save_learning_path.call_count == 2
