from unittest.mock import AsyncMock
import pytest

from src.features.assessments.update_question_status.update_question_status_handler import (
    UpdateQuestionStatusHandler,
)
from src.features.assessments.update_question_status.update_question_status_request import (
    UpdateQuestionStatusRequest,
)


@pytest.mark.asyncio
async def test_when_question_exists_and_status_updated_then_should_return_success():
    question_repository = AsyncMock()
    question_repository.update_question_status = AsyncMock(return_value=True)

    handler = UpdateQuestionStatusHandler(question_repository)
    request = UpdateQuestionStatusRequest(question_id="question_12345", status=True)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "Estado de pregunta actualizado exitosamente"
    assert response.question_id == "question_12345"
    assert response.new_status is True
    question_repository.update_question_status.assert_called_once_with(
        "question_12345", True
    )


@pytest.mark.asyncio
async def test_when_question_not_found_then_should_return_failure():
    question_repository = AsyncMock()
    question_repository.update_question_status = AsyncMock(return_value=False)

    handler = UpdateQuestionStatusHandler(question_repository)
    request = UpdateQuestionStatusRequest(question_id="nonexistent_123", status=True)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "Pregunta con ID nonexistent_123 no encontrada"
    assert response.question_id == ""
    assert response.new_status is False
    question_repository.update_question_status.assert_called_once_with(
        "nonexistent_123", True
    )


@pytest.mark.asyncio
async def test_when_updating_status_to_false_then_should_return_success():
    question_repository = AsyncMock()
    question_repository.update_question_status = AsyncMock(return_value=True)

    handler = UpdateQuestionStatusHandler(question_repository)
    request = UpdateQuestionStatusRequest(question_id="question_67890", status=False)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.new_status is False
    question_repository.update_question_status.assert_called_once_with(
        "question_67890", False
    )
