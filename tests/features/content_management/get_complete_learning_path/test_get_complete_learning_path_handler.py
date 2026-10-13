from unittest.mock import AsyncMock
import pytest

from src.features.content_management.get_complete_learning_path.get_complete_learning_path_handler import (
    GetCompleteLearningPathHandler,
)
from src.features.content_management.get_complete_learning_path.get_complete_learning_path_request import (
    GetCompleteLearningPathRequest,
)
from src.features.content_management.shared.learning_path_manager_service import (
    LearningPathManagerService,
    PaginatedLearningPathResponse,
    TopicSummary,
    ContentByTopic,
)


def _build_topic_summary(
    path_id: str = "path_1", topic: str = "Python Basics"
) -> TopicSummary:
    return TopicSummary(
        topic_path_id=path_id,
        topic=topic,
        contents=[
            ContentByTopic(
                content_id="content_1",
                title="Intro",
                description="Introduction",
                rating=4.5,
                is_completed=True,
            )
        ],
        progress=0.75,
        is_completed=False,
    )


@pytest.mark.asyncio
async def test_when_service_returns_items_should_return_success():
    topic_summary = _build_topic_summary()
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.get_complete_learning_path = AsyncMock(
        return_value=PaginatedLearningPathResponse(
            is_success=True,
            message="La ruta de aprendizaje ha sido recuperada con éxito",
            items=[topic_summary],
            total=1,
            page=0,
        )
    )

    handler = GetCompleteLearningPathHandler(learning_path_service)
    request = GetCompleteLearningPathRequest(user_id="user_123", page=0, page_size=10)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "La ruta de aprendizaje ha sido recuperada con éxito"
    assert response.learning_path is not None
    assert len(response.learning_path) == 1
    assert response.learning_path[0].topic_path_id == "path_1"
    assert response.learning_path[0].topic == "Python Basics"
    assert response.learning_path[0].progress == 0.75
    learning_path_service.get_complete_learning_path.assert_called_once_with(
        user_id="user_123", page=0, page_size=10
    )


@pytest.mark.asyncio
async def test_when_service_returns_empty_items_should_return_failure():
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.get_complete_learning_path = AsyncMock(
        return_value=PaginatedLearningPathResponse(
            is_success=False,
            message="La ruta de aprendizaje no fue encontrada",
            items=[],
            total=0,
            page=0,
        )
    )

    handler = GetCompleteLearningPathHandler(learning_path_service)
    request = GetCompleteLearningPathRequest(user_id="user_123")
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "La ruta de aprendizaje no fue encontrada"
    assert response.learning_path is None
    learning_path_service.get_complete_learning_path.assert_called_once_with(
        user_id="user_123", page=0, page_size=10
    )


@pytest.mark.asyncio
async def test_when_service_returns_none_should_return_failure():
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.get_complete_learning_path = AsyncMock(return_value=None)

    handler = GetCompleteLearningPathHandler(learning_path_service)
    request = GetCompleteLearningPathRequest(user_id="user_123")
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "La ruta de aprendizaje no fue encontrada"
    assert response.learning_path is None


@pytest.mark.asyncio
async def test_when_service_returns_multiple_items_should_return_all():
    items = [
        _build_topic_summary(path_id="path_1", topic="Python Basics"),
        _build_topic_summary(path_id="path_2", topic="Data Structures"),
        _build_topic_summary(path_id="path_3", topic="Algorithms"),
    ]
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.get_complete_learning_path = AsyncMock(
        return_value=PaginatedLearningPathResponse(
            is_success=True,
            message="La ruta de aprendizaje ha sido recuperada con éxito",
            items=items,
            total=3,
            page=0,
        )
    )

    handler = GetCompleteLearningPathHandler(learning_path_service)
    request = GetCompleteLearningPathRequest(user_id="user_123", page=0, page_size=10)
    response = await handler.handle(request)

    assert response.is_success is True
    assert len(response.learning_path) == 3
    assert response.learning_path[0].topic == "Python Basics"
    assert response.learning_path[1].topic == "Data Structures"
    assert response.learning_path[2].topic == "Algorithms"


@pytest.mark.asyncio
async def test_when_service_raises_exception_should_propagate():
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.get_complete_learning_path = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = GetCompleteLearningPathHandler(learning_path_service)
    request = GetCompleteLearningPathRequest(user_id="user_123")

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(request)


@pytest.mark.asyncio
async def test_when_pagination_params_differ_should_forward_correctly():
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.get_complete_learning_path = AsyncMock(
        return_value=PaginatedLearningPathResponse(
            is_success=True,
            message="La ruta de aprendizaje ha sido recuperada con éxito",
            items=[_build_topic_summary()],
            total=50,
            page=3,
        )
    )

    handler = GetCompleteLearningPathHandler(learning_path_service)
    request = GetCompleteLearningPathRequest(user_id="user_123", page=3, page_size=5)
    response = await handler.handle(request)

    assert response.is_success is True
    learning_path_service.get_complete_learning_path.assert_called_once_with(
        user_id="user_123", page=3, page_size=5
    )


@pytest.mark.asyncio
async def test_when_items_have_contents_should_preserve_content_details():
    topic_with_contents = TopicSummary(
        topic_path_id="path_1",
        topic="Python Basics",
        contents=[
            ContentByTopic(
                content_id="c1",
                title="Variables",
                description="Learn variables",
                rating=4.8,
                is_completed=True,
            ),
            ContentByTopic(
                content_id="c2",
                title="Functions",
                description="Learn functions",
                rating=4.2,
                is_completed=False,
            ),
        ],
        progress=0.5,
        is_completed=False,
    )
    learning_path_service = AsyncMock(spec=LearningPathManagerService)
    learning_path_service.get_complete_learning_path = AsyncMock(
        return_value=PaginatedLearningPathResponse(
            is_success=True,
            message="La ruta de aprendizaje ha sido recuperada con éxito",
            items=[topic_with_contents],
            total=1,
            page=0,
        )
    )

    handler = GetCompleteLearningPathHandler(learning_path_service)
    request = GetCompleteLearningPathRequest(user_id="user_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert len(response.learning_path[0].contents) == 2
    assert response.learning_path[0].contents[0].content_id == "c1"
    assert response.learning_path[0].contents[0].title == "Variables"
    assert response.learning_path[0].contents[0].is_completed is True
    assert response.learning_path[0].contents[1].content_id == "c2"
    assert response.learning_path[0].contents[1].is_completed is False
    assert response.learning_path[0].progress == 0.5
