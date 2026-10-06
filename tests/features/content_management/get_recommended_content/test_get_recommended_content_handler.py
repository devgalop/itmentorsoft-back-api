from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_recommended_content.get_recommended_content_handler import (
    GetRecommendedContentHandler,
)
from src.features.content_management.get_recommended_content.get_recommended_content_request import (
    GetRecommendedContentRequest,
)
from src.features.content_management.shared.learning_path_manager_service import (
    LearningPathManagerService,
    LearningPathResponse,
    TopicSummary,
    ContentByTopic,
)


@pytest.mark.asyncio
async def test_when_path_not_associated_should_return_failure():
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.check_path_association = AsyncMock(return_value=False)

    handler = GetRecommendedContentHandler(learning_path_service)
    request = GetRecommendedContentRequest(student_id="student_123", path_id="path_456")
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Error al recuperar la ruta de aprendizaje"
    assert response.recommendation is None
    learning_path_service.check_path_association.assert_called_once_with(
        "student_123", "path_456"
    )
    learning_path_service.get_learning_path.assert_not_called()


@pytest.mark.asyncio
async def test_when_service_returns_failure_should_return_failure_response():
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.check_path_association = AsyncMock(return_value=True)
    learning_path_service.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=False,
            message="La ruta de aprendizaje no fue encontrada",
            learning_path=None,
        )
    )

    handler = GetRecommendedContentHandler(learning_path_service)
    request = GetRecommendedContentRequest(student_id="student_123", path_id="path_456")
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Error al recuperar la ruta de aprendizaje"
    assert response.recommendation is None
    learning_path_service.check_path_association.assert_called_once_with(
        "student_123", "path_456"
    )
    learning_path_service.get_learning_path.assert_called_once_with("path_456")


@pytest.mark.asyncio
async def test_when_service_returns_success_should_return_topic_summary():
    topic_summary = TopicSummary(
        topic_path_id="path_456",
        topic="Python Programming",
        contents=[
            ContentByTopic(
                content_id="content_1",
                title="Intro to Python",
                description="Learn Python basics",
                rating=4.5,
            )
        ],
        progress=0.5,
    )

    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.check_path_association = AsyncMock(return_value=True)
    learning_path_service.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=True,
            message="La ruta de aprendizaje ha sido recuperada con éxito",
            learning_path=topic_summary,
        )
    )

    handler = GetRecommendedContentHandler(learning_path_service)
    request = GetRecommendedContentRequest(student_id="student_123", path_id="path_456")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Ruta de aprendizaje recuperada exitosamente"
    assert response.recommendation is not None
    assert response.recommendation.topic_path_id == "path_456"
    assert response.recommendation.topic == "Python Programming"
    assert len(response.recommendation.contents) == 1
    assert response.recommendation.contents[0].content_id == "content_1"
    assert response.recommendation.contents[0].title == "Intro to Python"
    assert response.recommendation.contents[0].rating == 4.5
    assert response.recommendation.progress == 0.5
    learning_path_service.check_path_association.assert_called_once_with(
        "student_123", "path_456"
    )
    learning_path_service.get_learning_path.assert_called_once_with("path_456")


@pytest.mark.asyncio
async def test_when_service_returns_none_should_return_failure():
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.check_path_association = AsyncMock(return_value=True)
    learning_path_service.get_learning_path = AsyncMock(return_value=None)

    handler = GetRecommendedContentHandler(learning_path_service)
    request = GetRecommendedContentRequest(student_id="student_123", path_id="path_456")
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Error al recuperar la ruta de aprendizaje"
    assert response.recommendation is None


@pytest.mark.asyncio
async def test_when_topic_has_multiple_contents_should_return_all():
    topic_summary = TopicSummary(
        topic_path_id="path_456",
        topic="Advanced Python",
        contents=[
            ContentByTopic(
                content_id="c1",
                title="Decorators",
                description="Learn decorators",
                rating=4.8,
            ),
            ContentByTopic(
                content_id="c2",
                title="Generators",
                description="Learn generators",
                rating=4.6,
            ),
            ContentByTopic(
                content_id="c3",
                title="Metaclasses",
                description="Learn metaclasses",
                rating=4.9,
            ),
        ],
        progress=0.33,
    )

    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.check_path_association = AsyncMock(return_value=True)
    learning_path_service.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=True,
            message="Success",
            learning_path=topic_summary,
        )
    )

    handler = GetRecommendedContentHandler(learning_path_service)
    request = GetRecommendedContentRequest(student_id="student_123", path_id="path_456")
    response = await handler.handle(request)

    assert response.is_success is True
    assert len(response.recommendation.contents) == 3
    assert response.recommendation.contents[0].content_id == "c1"
    assert response.recommendation.contents[1].content_id == "c2"
    assert response.recommendation.contents[2].content_id == "c3"
