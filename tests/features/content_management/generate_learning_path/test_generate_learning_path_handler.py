from unittest.mock import AsyncMock
import pytest

from src.features.content_management.generate_learning_path.generate_learning_path_handler import (
    GenerateLearningPathHandler,
)
from src.features.content_management.generate_learning_path.generate_learning_path_request import (
    GenerateLearningPathRequest,
)
from src.features.content_management.shared.learning_path_manager_service import (
    LearningPathCreatedResponse,
    TopicPathAssociation,
)


@pytest.mark.asyncio
async def test_when_service_returns_success_should_return_learning_path():
    learning_path_service = AsyncMock()
    learning_path_service.create_learning_path = AsyncMock(
        return_value=LearningPathCreatedResponse(
            is_success=True,
            message="Ruta de aprendizaje creada exitosamente",
            topic_paths=[
                TopicPathAssociation(topic_path_id="path_1", topic="Python Basics"),
                TopicPathAssociation(topic_path_id="path_2", topic="Data Structures"),
            ],
        )
    )

    handler = GenerateLearningPathHandler(learning_path_service)
    request = GenerateLearningPathRequest(student_id="student_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Ruta de aprendizaje creada exitosamente"
    assert response.learning_path is not None
    assert len(response.learning_path) == 2
    assert response.learning_path[0].topic_path_id == "path_1"
    assert response.learning_path[0].topic == "Python Basics"
    assert response.learning_path[1].topic_path_id == "path_2"
    assert response.learning_path[1].topic == "Data Structures"
    learning_path_service.create_learning_path.assert_called_once_with("student_123")


@pytest.mark.asyncio
async def test_when_service_returns_failure_should_return_error_response():
    learning_path_service = AsyncMock()
    learning_path_service.create_learning_path = AsyncMock(
        return_value=LearningPathCreatedResponse(
            is_success=False,
            message="Estudiante no encontrado",
            topic_paths=[],
        )
    )

    handler = GenerateLearningPathHandler(learning_path_service)
    request = GenerateLearningPathRequest(student_id="invalid_student")
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Estudiante no encontrado"
    assert response.learning_path is None
    learning_path_service.create_learning_path.assert_called_once_with(
        "invalid_student"
    )


@pytest.mark.asyncio
async def test_when_learning_path_already_exists_should_return_failure():
    learning_path_service = AsyncMock()
    learning_path_service.create_learning_path = AsyncMock(
        return_value=LearningPathCreatedResponse(
            is_success=False,
            message="La ruta de aprendizaje ya existe y no está completada. Debe completarla antes de crear una nueva",
            topic_paths=[],
        )
    )

    handler = GenerateLearningPathHandler(learning_path_service)
    request = GenerateLearningPathRequest(student_id="student_456")
    response = await handler.handle(request)

    assert response.is_success is False
    assert (
        response.message
        == "La ruta de aprendizaje ya existe y no está completada. Debe completarla antes de crear una nueva"
    )
    assert response.learning_path is None


@pytest.mark.asyncio
async def test_when_service_returns_empty_topic_paths_should_return_empty_list():
    learning_path_service = AsyncMock()
    learning_path_service.create_learning_path = AsyncMock(
        return_value=LearningPathCreatedResponse(
            is_success=True,
            message="Ruta de aprendizaje creada exitosamente",
            topic_paths=[],
        )
    )

    handler = GenerateLearningPathHandler(learning_path_service)
    request = GenerateLearningPathRequest(student_id="student_789")
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.learning_path == []


@pytest.mark.asyncio
async def test_when_service_raises_exception_should_propagate():
    learning_path_service = AsyncMock()
    learning_path_service.create_learning_path = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = GenerateLearningPathHandler(learning_path_service)
    request = GenerateLearningPathRequest(student_id="student_123")

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(request)


@pytest.mark.asyncio
async def test_when_service_returns_single_topic_path_should_return_single_item():
    learning_path_service = AsyncMock()
    learning_path_service.create_learning_path = AsyncMock(
        return_value=LearningPathCreatedResponse(
            is_success=True,
            message="Ruta de aprendizaje creada exitosamente",
            topic_paths=[
                TopicPathAssociation(
                    topic_path_id="path_single", topic="Advanced Python"
                ),
            ],
        )
    )

    handler = GenerateLearningPathHandler(learning_path_service)
    request = GenerateLearningPathRequest(student_id="student_123")
    response = await handler.handle(request)

    assert response.is_success is True
    assert len(response.learning_path) == 1
    assert response.learning_path[0].topic == "Advanced Python"
    assert response.learning_path[0].topic_path_id == "path_single"
