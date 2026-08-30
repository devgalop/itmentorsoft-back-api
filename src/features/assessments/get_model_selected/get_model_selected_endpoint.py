from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_model_selected.get_model_selected_handler import (
    GetModelSelectedHandler,
)
from src.features.assessments.get_model_selected.get_model_selected_response import (
    GetModelSelectedResponse,
)
from src.features.assessments.shared.dependencies import get_get_model_selected_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/model_selected",
    status_code=200,
    summary="Get selected models for each process",
    description="Endpoint to retrieve the selected models for each available process.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Selected models retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Successfully retrieved selected models.",
                        "models_by_process": [
                            {"process": "QUALIFIER", "model_id": "minimax-m2.7"},
                            {"process": "EXPLORER", "model_id": "explorer-v1.0"},
                        ],
                    }
                }
            },
        },
        400: {
            "description": "Failed to retrieve selected models.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Failed to retrieve selected models: <error_message>",
                        "models_by_process": [],
                    }
                }
            },
        },
    },
)
def get_model_selected(
    handler: Annotated[
        GetModelSelectedHandler, Depends(get_get_model_selected_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> GetModelSelectedResponse:
    response = handler.handle()
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
