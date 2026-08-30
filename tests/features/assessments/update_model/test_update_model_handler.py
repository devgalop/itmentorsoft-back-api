from unittest.mock import AsyncMock, Mock
import pytest

from src.features.assessments.update_model.update_model_handler import (
    UpdateModelHandler,
)
from src.features.assessments.update_model.update_model_request import (
    UpdateModelRequest,
)
from src.features.assessments.shared.qualifier_service import (
    AvailableProcesses,
    ModelSelectorService,
    ModelExplorerService,
)


@pytest.mark.asyncio
async def test_when_valid_request_should_update_model():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_explorer_service = Mock(spec=ModelExplorerService)

    model_explorer_service.get_available_models = AsyncMock(
        return_value=["model-1", "model-2", "model-3"]
    )
    model_selector_service.set_selected_model = AsyncMock()

    handler = UpdateModelHandler(model_selector_service, model_explorer_service)
    response = await handler.handle(
        UpdateModelRequest(process="qualifier", model_id="model-2")
    )

    assert response.is_success is True
    assert response.message == "Model updated successfully"
    model_explorer_service.get_available_models.assert_called_once()
    model_selector_service.set_selected_model.assert_called_once()


@pytest.mark.asyncio
async def test_when_process_is_invalid_should_return_failure():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_explorer_service = Mock(spec=ModelExplorerService)

    handler = UpdateModelHandler(model_selector_service, model_explorer_service)
    response = await handler.handle(
        UpdateModelRequest(process="invalid_process", model_id="model-1")
    )

    assert response.is_success is False
    assert response.message == "Invalid process specified"
    model_explorer_service.get_available_models.assert_not_called()
    model_selector_service.set_selected_model.assert_not_called()


@pytest.mark.asyncio
async def test_when_model_not_available_should_return_failure():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_explorer_service = Mock(spec=ModelExplorerService)

    model_explorer_service.get_available_models = AsyncMock(
        return_value=["model-1", "model-2"]
    )

    handler = UpdateModelHandler(model_selector_service, model_explorer_service)
    response = await handler.handle(
        UpdateModelRequest(process="qualifier", model_id="non-existent-model")
    )

    assert response.is_success is False
    assert response.message == "Model ID not found in available models"
    model_explorer_service.get_available_models.assert_called_once()
    model_selector_service.set_selected_model.assert_not_called()


@pytest.mark.asyncio
async def test_when_service_raises_exception_should_return_failure():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_explorer_service = Mock(spec=ModelExplorerService)

    model_explorer_service.get_available_models = AsyncMock(
        side_effect=Exception("Connection failed")
    )

    handler = UpdateModelHandler(model_selector_service, model_explorer_service)
    response = await handler.handle(
        UpdateModelRequest(process="qualifier", model_id="model-1")
    )

    assert response.is_success is False
    assert response.message == "Connection failed"


@pytest.mark.asyncio
async def test_handler_calls_services_with_correct_parameters():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_explorer_service = Mock(spec=ModelExplorerService)

    model_explorer_service.get_available_models = AsyncMock(
        return_value=["model-1", "model-2"]
    )
    model_selector_service.set_selected_model = AsyncMock()

    handler = UpdateModelHandler(model_selector_service, model_explorer_service)
    await handler.handle(UpdateModelRequest(process="classifier", model_id="model-2"))

    model_selector_service.set_selected_model.assert_called_once_with(
        process=AvailableProcesses.CLASSIFIER, model_name="model-2"
    )
