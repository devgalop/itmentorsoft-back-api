from src.features.assessments.get_available_models.get_available_models_response import (
    GetAvailableModelsResponse,
)
from src.features.assessments.shared.qualifier_service import (
    QualifierModelsService,
)


class GetAvailableModelsHandler:
    def __init__(self, qualifier_service: QualifierModelsService):
        self.qualifier_service = qualifier_service

    async def handle(self) -> GetAvailableModelsResponse:
        try:
            models = await self.qualifier_service.get_available_models()
            if not models:
                return GetAvailableModelsResponse(
                    is_success=False, message="No available models found.", models=[]
                )
            return GetAvailableModelsResponse(
                is_success=True,
                message="Successfully fetched available models.",
                models=models,
            )
        except Exception as e:
            return GetAvailableModelsResponse(
                is_success=False,
                message=f"Failed to fetch available models: {str(e)}",
                models=[],
            )
