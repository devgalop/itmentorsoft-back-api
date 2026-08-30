from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.shared.dependencies import get_update_model_handler
from src.features.assessments.update_model.update_model_handler import (
    UpdateModelHandler,
)
from src.features.assessments.update_model.update_model_request import (
    UpdateModelRequest,
)
from src.features.assessments.update_model.update_model_response import (
    UpdateModelResponse,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.put(
    "/models",
    summary="Update the model for a specific process",
    description="Endpoint to update the model for a specific process.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Model updated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Model updated successfully",
                    }
                }
            },
        },
        400: {
            "description": "Invalid request data.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Invalid request data."}
                }
            },
        },
        401: {
            "description": "Unauthorized.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Unauthorized."}
                }
            },
        },
        404: {
            "description": "Model not found.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Model not found"}
                }
            },
        },
    },
)
async def update_model(
    request: UpdateModelRequest,
    handler: Annotated[UpdateModelHandler, Depends(get_update_model_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> UpdateModelResponse:
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
