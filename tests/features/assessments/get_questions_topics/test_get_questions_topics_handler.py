from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_questions_topics.get_questions_topics_handler import (
    GetQuestionsTopicsHandler,
)


@pytest.mark.asyncio
async def test_when_topics_exist_should_return_success():
    question_repository = AsyncMock()
    question_repository.get_questions_topics = AsyncMock(
        return_value=["Math", "Science", "History"]
    )

    handler = GetQuestionsTopicsHandler(question_repository)
    response = await handler.handle()

    assert response.is_success is True
    assert response.message == "Temas publicados obtenidos exitosamente"
    assert response.topics == ["Math", "Science", "History"]
    question_repository.get_questions_topics.assert_called_once()


@pytest.mark.asyncio
async def test_when_topics_is_empty_should_return_failure():
    question_repository = AsyncMock()
    question_repository.get_questions_topics = AsyncMock(return_value=[])

    handler = GetQuestionsTopicsHandler(question_repository)
    response = await handler.handle()

    assert response.is_success is False
    assert response.message == "No se encontraron temas"
    assert response.topics == []
    question_repository.get_questions_topics.assert_called_once()


@pytest.mark.asyncio
async def test_when_repository_returns_single_topic_should_return_success():
    question_repository = AsyncMock()
    question_repository.get_questions_topics = AsyncMock(return_value=["Programming"])

    handler = GetQuestionsTopicsHandler(question_repository)
    response = await handler.handle()

    assert response.is_success is True
    assert response.topics == ["Programming"]
    assert len(response.topics) == 1


@pytest.mark.asyncio
async def test_when_repository_returns_many_topics_should_return_all():
    question_repository = AsyncMock()
    many_topics = [f"Topic_{i}" for i in range(50)]
    question_repository.get_questions_topics = AsyncMock(return_value=many_topics)

    handler = GetQuestionsTopicsHandler(question_repository)
    response = await handler.handle()

    assert response.is_success is True
    assert len(response.topics) == 50
    assert response.topics == many_topics


@pytest.mark.asyncio
async def test_when_repository_raises_exception_should_propagate():
    question_repository = AsyncMock()
    question_repository.get_questions_topics = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = GetQuestionsTopicsHandler(question_repository)

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle()
