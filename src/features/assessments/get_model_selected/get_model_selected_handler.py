from src.features.assessments.get_model_selected.get_model_selected_response import (
    GetModelSelectedResponse,
    ModelByProcess,
)
from src.features.assessments.shared.qualifier_service import (
    AvailableProcesses,
    ModelSelectorService,
)


class GetModelSelectedHandler:

    def __init__(self, model_selector_service: ModelSelectorService):
        self.model_selector_service = model_selector_service

    def handle(self) -> GetModelSelectedResponse:
        try:
            models_by_process = [
                ModelByProcess(
                    process=process.value,
                    model_id=self.model_selector_service.get_selected_model(process),
                )
                for process in AvailableProcesses
            ]

            if not models_by_process:
                return GetModelSelectedResponse(
                    is_success=False,
                    message="No selected models found.",
                    models_by_process=[],
                )
            return GetModelSelectedResponse(
                is_success=True,
                message="Successfully retrieved selected models.",
                models_by_process=models_by_process,
            )
        except Exception as e:
            return GetModelSelectedResponse(
                is_success=False,
                message=f"Failed to retrieve selected models: {str(e)}",
                models_by_process=[],
            )
