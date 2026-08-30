from src.features.assessments.shared.qualifier_service import (
    AvailableProcesses,
    ModelExplorerService,
    ModelSelectorService,
)
from src.features.assessments.update_model.update_model_request import (
    UpdateModelRequest,
)
from src.features.assessments.update_model.update_model_response import (
    UpdateModelResponse,
)


class UpdateModelHandler:
    def __init__(
        self,
        model_selector_service: ModelSelectorService,
        model_explorer_service: ModelExplorerService,
    ):
        self.model_selector_service = model_selector_service
        self.model_explorer_service = model_explorer_service

    async def handle(self, request: UpdateModelRequest) -> UpdateModelResponse:
        try:
            if request.process not in [process.value for process in AvailableProcesses]:
                return UpdateModelResponse(
                    is_success=False, message="Invalid process specified"
                )

            process = AvailableProcesses(request.process)

            available_models = await self.model_explorer_service.get_available_models()
            if request.model_id not in available_models:
                return UpdateModelResponse(
                    is_success=False, message="Model ID not found in available models"
                )

            await self.model_selector_service.set_selected_model(
                process=process, model_name=request.model_id
            )
            return UpdateModelResponse(
                is_success=True, message="Model updated successfully"
            )
        except Exception as e:
            return UpdateModelResponse(is_success=False, message=str(e))
