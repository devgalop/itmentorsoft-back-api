from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.shared.dependencies import get_models_service
from src.features.assessments.shared.qualifier_service import ModelExplorerService

router = APIRouter()


@router.get(
    "/health",
    status_code=200,
    summary="Health check endpoint",
    description="Endpoint to check the health status of the application",
    tags=["Health Check"],
    responses={200: {"status": "healthy"}, 503: {"status": "unhealthy"}},
)
async def health_check(
    model_explorer_service: Annotated[
        ModelExplorerService, Depends(get_models_service)
    ],
):
    models = model_explorer_service.get_available_models()
    if not models:
        raise HTTPException(status_code=503, detail='{"status": "unhealthy"}')
    return {"status": "healthy"}
