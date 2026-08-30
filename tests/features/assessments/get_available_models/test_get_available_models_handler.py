from unittest.mock import AsyncMock
import pytest

from src.features.assessments.get_available_models.get_available_models_handler import (
    GetAvailableModelsHandler,
)


@pytest.mark.asyncio
async def test_when_models_are_available_should_return_success_response():
    qualifier_service = AsyncMock()
    qualifier_service.get_available_models = AsyncMock(
        return_value=["gpt-4", "gpt-3.5-turbo", "claude-3"]
    )

    handler = GetAvailableModelsHandler(qualifier_service)
    response = await handler.handle()

    assert response.is_success is True
    assert response.message == "Successfully fetched available models."
    assert response.models == ["gpt-4", "gpt-3.5-turbo", "claude-3"]
    qualifier_service.get_available_models.assert_called_once()


@pytest.mark.asyncio
async def test_when_no_models_are_available_should_return_failure_response():
    qualifier_service = AsyncMock()
    qualifier_service.get_available_models = AsyncMock(return_value=[])

    handler = GetAvailableModelsHandler(qualifier_service)
    response = await handler.handle()

    assert response.is_success is False
    assert response.message == "No available models found."
    assert response.models == []
    qualifier_service.get_available_models.assert_called_once()


@pytest.mark.asyncio
async def test_when_service_throws_exception_should_return_failure_response():
    qualifier_service = AsyncMock()
    qualifier_service.get_available_models = AsyncMock(
        side_effect=Exception("Connection timeout")
    )

    handler = GetAvailableModelsHandler(qualifier_service)
    response = await handler.handle()

    assert response.is_success is False
    assert response.message == "Failed to fetch available models: Connection timeout"
    assert response.models == []
    qualifier_service.get_available_models.assert_called_once()
