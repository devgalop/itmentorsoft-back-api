from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_question_categories.get_question_categories_handler import (
    GetQuestionCategoriesHandler,
)
from src.features.assessments.get_question_categories.get_question_categories_request import (
    GetQuestionCategoriesRequest,
)

VERSION = 1


@pytest.mark.asyncio
async def test_when_categories_exist_then_should_return_categories_successfully():
    question_repository = AsyncMock()
    question_repository.get_question_categories = AsyncMock(
        return_value=["Fundamentos y paradigmas", "Programación orientada a objetos"]
    )

    handler = GetQuestionCategoriesHandler(question_repository)

    request = GetQuestionCategoriesRequest(version=VERSION)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Categorías de preguntas obtenidas exitosamente"
    assert len(response.categories) == 2


@pytest.mark.asyncio
async def test_when_categories_is_empty_then_should_return_failure():
    question_repository = AsyncMock()
    question_repository.get_question_categories = AsyncMock(return_value=[])

    handler = GetQuestionCategoriesHandler(question_repository)

    request = GetQuestionCategoriesRequest(version=VERSION)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "No se pudieron obtener las categorías de preguntas"
    assert response.categories == []


@pytest.mark.asyncio
async def test_when_categories_is_none_then_should_return_failure():
    question_repository = AsyncMock()
    question_repository.get_question_categories = AsyncMock(return_value=None)

    handler = GetQuestionCategoriesHandler(question_repository)

    request = GetQuestionCategoriesRequest(version=VERSION)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "No se pudieron obtener las categorías de preguntas"
    assert response.categories == []


@pytest.mark.asyncio
async def test_calls_repository_with_correct_version():
    question_repository = AsyncMock()
    question_repository.get_question_categories = AsyncMock(return_value=["Category A"])

    handler = GetQuestionCategoriesHandler(question_repository)

    request = GetQuestionCategoriesRequest(version=VERSION)
    await handler.handle(request)

    question_repository.get_question_categories.assert_called_once_with(VERSION)


@pytest.mark.asyncio
async def test_when_repository_raises_then_handler_propagates_exception():
    question_repository = AsyncMock()
    question_repository.get_question_categories = AsyncMock(
        side_effect=Exception("Database error")
    )

    handler = GetQuestionCategoriesHandler(question_repository)

    request = GetQuestionCategoriesRequest(version=VERSION)

    with pytest.raises(Exception, match="Database error"):
        await handler.handle(request)
