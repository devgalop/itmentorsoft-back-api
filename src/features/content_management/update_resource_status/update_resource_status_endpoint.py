from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.shared.dependencies import (
    get_update_resource_status_handler,
)
from src.features.content_management.update_resource_status.update_resource_status_handler import (
    UpdateResourceStatusHandler,
)
from src.features.content_management.update_resource_status.update_resource_status_request import (
    UpdateResourceStatusRequest,
)
from src.features.content_management.update_resource_status.update_resource_status_response import (
    UpdateResourceStatusResponse,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.put(
    "/update/status",
    status_code=200,
    summary="Update the status of a resource",
    description="This endpoint allows updating the status of a resource in the content management system.",
    tags=["Content Management"],
    responses={
        200: {"description": "Resource status updated successfully."},
        400: {"description": "Invalid input data."},
        404: {"description": "Resource not found."},
        500: {"description": "Internal server error."},
    },
)
async def update_resource_status(
    request: UpdateResourceStatusRequest,
    handler: Annotated[
        UpdateResourceStatusHandler, Depends(get_update_resource_status_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> UpdateResourceStatusResponse:
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.message)
    return response
