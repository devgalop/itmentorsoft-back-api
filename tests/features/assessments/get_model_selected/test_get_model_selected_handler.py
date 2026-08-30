from unittest.mock import Mock

from src.features.assessments.get_model_selected.get_model_selected_handler import (
    GetModelSelectedHandler,
)
from src.features.assessments.get_model_selected.get_model_selected_response import (
    GetModelSelectedResponse,
)
from src.features.assessments.shared.qualifier_service import (
    AvailableProcesses,
    ModelSelectorService,
)


def test_when_service_returns_models_should_return_success():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_selector_service.get_selected_model = Mock(
        side_effect=lambda process: {
            AvailableProcesses.QUALIFIER: "minimax-m2.7",
            AvailableProcesses.CLASSIFIER: "classifier-v1.0",
        }[process]
    )

    handler = GetModelSelectedHandler(model_selector_service)
    response = handler.handle()

    assert isinstance(response, GetModelSelectedResponse)
    assert response.is_success is True
    assert response.message == "Successfully retrieved selected models."
    assert len(response.models_by_process) == len(AvailableProcesses)

    qualifier_model = next(
        m for m in response.models_by_process if m.process == "qualifier"
    )
    assert qualifier_model.model_id == "minimax-m2.7"

    classifier_model = next(
        m for m in response.models_by_process if m.process == "classifier"
    )
    assert classifier_model.model_id == "classifier-v1.0"


def test_when_service_raises_exception_should_return_failure():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_selector_service.get_selected_model = Mock(
        side_effect=RuntimeError("Connection failed")
    )

    handler = GetModelSelectedHandler(model_selector_service)
    response = handler.handle()

    assert isinstance(response, GetModelSelectedResponse)
    assert response.is_success is False
    assert "Connection failed" in response.message
    assert response.models_by_process == []


def test_handler_calls_service_for_each_process():
    model_selector_service = Mock(spec=ModelSelectorService)
    model_selector_service.get_selected_model = Mock(return_value="test-model")

    handler = GetModelSelectedHandler(model_selector_service)
    handler.handle()

    assert model_selector_service.get_selected_model.call_count == len(
        AvailableProcesses
    )
    for process in AvailableProcesses:
        model_selector_service.get_selected_model.assert_any_call(process)
