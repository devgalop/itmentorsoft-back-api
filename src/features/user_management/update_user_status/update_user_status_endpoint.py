from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.features.user_management.shared.dependencies import (
    get_update_user_status_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData
from src.features.user_management.update_user_status.update_user_status_handler import (
    UpdateUserStatusHandler,
)
from src.features.user_management.update_user_status.update_user_status_request import (
    UpdateUserStatusRequest,
)
from src.features.user_management.update_user_status.update_user_status_response import (
    UpdateUserStatusResponse,
)

router = APIRouter()


@router.put(
    "/user-status",
    status_code=200,
    summary="Update user status",
    description="Update the status of a user.",
    tags=["User Management"],
    responses={
        200: {
            "description": "User status updated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "User status updated successfully",
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
            "description": "User not found.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "User not found."}
                }
            },
        },
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Internal server error.",
                    }
                }
            },
        },
    },
)
async def update_user_status(
    request: UpdateUserStatusRequest,
    handler: Annotated[
        UpdateUserStatusHandler, Depends(get_update_user_status_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> UpdateUserStatusResponse:
    try:
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=400, detail=response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
