from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.features.reports.get_users_by_role.get_users_by_role_handler import (
    GetUsersByRoleHandler,
)
from src.features.reports.get_users_by_role.get_users_by_role_request import (
    GetUsersByRoleRequest,
)
from src.features.reports.get_users_by_role.get_users_by_role_response import (
    GetUsersByRoleResponse,
)
from src.features.reports.shared.dependencies import get_get_users_by_role_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/users-by-role",
    status_code=200,
    summary="Get users by role",
    description="Retrieve a list of users filtered by their role.",
    tags=["Reports"],
    responses={
        200: {
            "description": "Users retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Users retrieved successfully",
                        "users": [{"user_id": 1, "role": "admin"}],
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
async def get_users_by_role(
    role: str,
    handler: Annotated[GetUsersByRoleHandler, Depends(get_get_users_by_role_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> GetUsersByRoleResponse:
    """Endpoint to retrieve users filtered by their role.

    Args:
        role (str): The role to filter users by.
        handler (GetUsersByRoleHandler): The handler responsible for processing the request.
        _ (TokenData): Token data for authentication and authorization.

    Returns:
        GetUsersByRoleResponse: Response object containing the result of the query.
    """
    try:
        request = GetUsersByRoleRequest(role=role)
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=400, detail=response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
