from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_available_models.get_available_models_handler import (
    GetAvailableModelsHandler,
)
from src.features.assessments.get_available_models.get_available_models_response import (
    GetAvailableModelsResponse,
)
from src.features.assessments.shared.dependencies import (
    get_get_available_models_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/available_models",
    status_code=200,
    summary="Get available models",
    description="Endpoint to retrieve the list of available models from the LLM Provider.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Available models retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Successfully fetched available models.",
                        "models": ["model_1", "model_2", "model_3"],
                    }
                }
            },
        },
        400: {
            "description": "Failed to fetch available models.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Failed to fetch available models: <error_message>",
                        "models": [],
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized access. User must be authenticated.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Unauthorized."}
                }
            },
        },
        500: {
            "description": "Failed to fetch available models.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Failed to fetch available models: <error_message>",
                        "models": [],
                    }
                }
            },
        },
    },
)
async def get_available_models(
    handler: Annotated[
        GetAvailableModelsHandler, Depends(get_get_available_models_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> GetAvailableModelsResponse:
    """Endpoint to retrieve the list of available models from the LLM Provider."""
    try:
        response = await handler.handle()
        if not response.is_success:
            raise HTTPException(status_code=400, detail=response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch available models: {str(e)}"
        )
