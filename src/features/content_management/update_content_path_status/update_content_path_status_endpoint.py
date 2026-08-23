from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.shared.dependencies import (
    get_update_content_path_status_handler,
)
from src.features.content_management.update_content_path_status.update_content_path_status_handler import (
    UpdateContentPathStatusHandler,
)
from src.features.content_management.update_content_path_status.update_content_path_status_request import (
    UpdateContentPathStatusRequest,
)
from src.features.content_management.update_content_path_status.update_content_path_status_response import (
    UpdateContentPathStatusResponse,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.put(
    "/learning-path/update/status",
    status_code=200,
    summary="Update content path status",
    description="Endpoint to update the status of a content path within a learning path.",
    tags=["Learning Path Management"],
    responses={
        200: {
            "description": "Content path status updated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Content path status updated successfully.",
                        "path_progress": 0.75,
                    }
                }
            },
        },
        400: {
            "description": "Invalid request parameters.",
            "content": {
                "application/json": {
                    "example": {"message": "Invalid request parameters."}
                }
            },
        },
        401: {
            "description": "Unauthorized.",
            "content": {"application/json": {"example": {"message": "Unauthorized."}}},
        },
        404: {
            "description": "Not Found. Content path or learning path not found.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Content path not found.",
                        "path_progress": None,
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error.",
            "content": {
                "application/json": {
                    "example": {"message": "An unexpected error occurred."}
                }
            },
        },
    },
)
async def update_content_path_status(
    request: UpdateContentPathStatusRequest,
    handler: Annotated[
        UpdateContentPathStatusHandler, Depends(get_update_content_path_status_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["student"]))],
) -> UpdateContentPathStatusResponse:
    try:
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
