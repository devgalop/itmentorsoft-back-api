from unittest.mock import AsyncMock
import pytest

from src.features.content_management.shared.learning_path_manager_service import (
    LearningPathManagerService,
)
from itmentorsoft_persistence.dto import (
    LearningPath,
    LearningPathResponse,
    ContentByTopic,
)

# ============================================================================
# create_learning_path tests
# ============================================================================


@pytest.mark.asyncio
async def test_create_learning_path_when_user_not_found_should_return_failure():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value=None)
    learning_path_repository = AsyncMock()

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.create_learning_path("invalid_user")

    assert response.is_success is False
    assert response.message == "Estudiante no encontrado"
    assert response.topic_paths == []
    user_repository.get_user_by_id.assert_called_once_with("invalid_user")
    learning_path_repository.is_learning_path_created.assert_not_called()


@pytest.mark.asyncio
async def test_create_learning_path_when_already_exists_should_return_failure():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value={"id": "user_123"})
    learning_path_repository = AsyncMock()
    learning_path_repository.is_learning_path_created = AsyncMock(return_value=True)

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.create_learning_path("user_123")

    assert response.is_success is False
    assert (
        response.message
        == "La ruta de aprendizaje ya existe y no está completada. Debe completarla antes de crear una nueva"
    )
    assert response.topic_paths == []
    user_repository.get_user_by_id.assert_called_once_with("user_123")
    learning_path_repository.is_learning_path_created.assert_called_once_with(
        "user_123"
    )
    learning_path_repository.get_learning_path.assert_not_called()


@pytest.mark.asyncio
async def test_create_learning_path_when_generation_fails_should_return_failure():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value={"id": "user_123"})
    learning_path_repository = AsyncMock()
    learning_path_repository.is_learning_path_created = AsyncMock(return_value=False)
    learning_path_repository.get_learning_path = AsyncMock(return_value=None)

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.create_learning_path("user_123")

    assert response.is_success is False
    assert response.message == "Error al crear la ruta de aprendizaje"
    assert response.topic_paths == []


@pytest.mark.asyncio
async def test_create_learning_path_when_success_should_save_and_return_paths():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value={"id": "user_123"})

    learning_path_repository = AsyncMock()
    learning_path_repository.is_learning_path_created = AsyncMock(return_value=False)
    learning_path_repository.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=True,
            message="Learning paths generated.",
            path_id="main_path",
            recommendation=[
                LearningPath(
                    path_id="path_1",
                    user_id="user_123",
                    topic="Python",
                    is_completed=False,
                    contents=[
                        ContentByTopic(
                            content_id="c1",
                            title="Intro to Python",
                            description="Basics",
                            rating=4.5,
                        )
                    ],
                ),
                LearningPath(
                    path_id="path_2",
                    user_id="user_123",
                    topic="Data Structures",
                    is_completed=False,
                    contents=[],
                ),
            ],
        )
    )
    learning_path_repository.save_learning_path = AsyncMock()

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.create_learning_path("user_123")

    assert response.is_success is True
    assert response.message == "Ruta de aprendizaje creada exitosamente"
    assert len(response.topic_paths) == 2
    assert response.topic_paths[0].topic_path_id == "path_1"
    assert response.topic_paths[0].topic == "Python"
    assert response.topic_paths[1].topic_path_id == "path_2"
    assert response.topic_paths[1].topic == "Data Structures"
    assert learning_path_repository.save_learning_path.call_count == 2


@pytest.mark.asyncio
async def test_create_learning_path_when_empty_recommendation_should_return_empty():
    user_repository = AsyncMock()
    user_repository.get_user_by_id = AsyncMock(return_value={"id": "user_123"})

    learning_path_repository = AsyncMock()
    learning_path_repository.is_learning_path_created = AsyncMock(return_value=False)
    learning_path_repository.get_learning_path = AsyncMock(
        return_value=LearningPathResponse(
            is_success=True,
            message="No recommendations found.",
            path_id="",
            recommendation=[],
        )
    )
    learning_path_repository.save_learning_path = AsyncMock()

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.create_learning_path("user_123")

    assert response.is_success is True
    assert response.topic_paths == []
    learning_path_repository.save_learning_path.assert_not_called()


# ============================================================================
# check_path_association tests
# ============================================================================


@pytest.mark.asyncio
async def test_check_path_association_when_associated_should_return_true():
    user_repository = AsyncMock()
    learning_path_repository = AsyncMock()
    learning_path_repository.is_path_associated_with_user = AsyncMock(return_value=True)

    service = LearningPathManagerService(user_repository, learning_path_repository)
    result = await service.check_path_association("user_123", "path_456")

    assert result is True
    learning_path_repository.is_path_associated_with_user.assert_called_once_with(
        "path_456", "user_123"
    )


@pytest.mark.asyncio
async def test_check_path_association_when_not_associated_should_return_false():
    user_repository = AsyncMock()
    learning_path_repository = AsyncMock()
    learning_path_repository.is_path_associated_with_user = AsyncMock(
        return_value=False
    )

    service = LearningPathManagerService(user_repository, learning_path_repository)
    result = await service.check_path_association("user_123", "path_999")

    assert result is False
    learning_path_repository.is_path_associated_with_user.assert_called_once_with(
        "path_999", "user_123"
    )


# ============================================================================
# get_learning_path tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_learning_path_when_not_found_should_return_failure():
    user_repository = AsyncMock()
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_by_id = AsyncMock(return_value=None)

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.get_learning_path("invalid_path")

    assert response.is_success is False
    assert response.message == "La ruta de aprendizaje no fue encontrada"
    assert response.learning_path is None
    learning_path_repository.get_learning_path_by_id.assert_called_once_with(
        "invalid_path"
    )


@pytest.mark.asyncio
async def test_get_learning_path_when_found_should_return_topic_summary():
    user_repository = AsyncMock()
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_by_id = AsyncMock(
        return_value=LearningPath(
            path_id="path_123",
            user_id="user_456",
            topic="Python Programming",
            is_completed=False,
            progress=0.5,
            contents=[
                ContentByTopic(
                    content_id="c1",
                    title="Variables",
                    description="Learn about variables",
                    rating=4.8,
                ),
                ContentByTopic(
                    content_id="c2",
                    title="Functions",
                    description="Learn about functions",
                    rating=4.6,
                ),
            ],
        )
    )

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.get_learning_path("path_123")

    assert response.is_success is True
    assert response.message == "La ruta de aprendizaje ha sido recuperada con éxito"
    assert response.learning_path is not None
    assert response.learning_path.topic_path_id == "path_123"
    assert response.learning_path.topic == "Python Programming"
    assert response.learning_path.progress == 0.5
    assert len(response.learning_path.contents) == 2
    assert response.learning_path.contents[0].content_id == "c1"
    assert response.learning_path.contents[0].title == "Variables"
    assert response.learning_path.contents[0].rating == 4.8
    assert response.learning_path.contents[1].content_id == "c2"
    assert response.learning_path.contents[1].title == "Functions"


@pytest.mark.asyncio
async def test_get_learning_path_with_no_contents_should_return_empty_list():
    user_repository = AsyncMock()
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_by_id = AsyncMock(
        return_value=LearningPath(
            path_id="path_empty",
            user_id="user_456",
            topic="Empty Topic",
            is_completed=False,
            progress=0.0,
            contents=[],
        )
    )

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.get_learning_path("path_empty")

    assert response.is_success is True
    assert response.learning_path.contents == []


@pytest.mark.asyncio
async def test_get_learning_path_with_completed_progress_should_return_full_progress():
    user_repository = AsyncMock()
    learning_path_repository = AsyncMock()
    learning_path_repository.get_learning_path_by_id = AsyncMock(
        return_value=LearningPath(
            path_id="path_complete",
            user_id="user_456",
            topic="Completed Topic",
            is_completed=True,
            progress=100.0,
            contents=[
                ContentByTopic(
                    content_id="c1",
                    title="Done Content",
                    description="Already done",
                    rating=5.0,
                )
            ],
        )
    )

    service = LearningPathManagerService(user_repository, learning_path_repository)
    response = await service.get_learning_path("path_complete")

    assert response.is_success is True
    assert response.learning_path.progress == 100.0
