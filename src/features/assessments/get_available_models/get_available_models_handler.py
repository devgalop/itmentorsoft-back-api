from src.i18n import t
from src.features.assessments.get_available_models.get_available_models_response import (
    GetAvailableModelsResponse,
)
from src.features.assessments.shared.qualifier_service import ModelExplorerService


class GetAvailableModelsHandler:
    def __init__(self, explorer_service: ModelExplorerService):
        self.explorer_service = explorer_service

    async def handle(self) -> GetAvailableModelsResponse:
        try:
            models = await self.explorer_service.get_available_models()
            if not models:
                return GetAvailableModelsResponse(
                    is_success=False, message=t("model.available.none_found"), models=[]
                )
            return GetAvailableModelsResponse(
                is_success=True,
                message=t("model.available.retrieved"),
                models=models,
            )
        except Exception as e:
            return GetAvailableModelsResponse(
                is_success=False,
                message=t("model.available.retrieval_failed", error=str(e)),
                models=[],
            )
