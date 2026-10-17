from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.user_management.create_user_from_admin.create_user_from_admin_handler import (
    CreateUserFromAdminHandler,
)
from src.features.user_management.create_user_from_admin.create_user_from_admin_request import (
    CreateUserFromAdminRequest,
)
from src.features.user_management.create_user_from_admin.create_user_from_admin_response import (
    CreateUserFromAdminResponse,
)
from src.features.user_management.shared.dependencies import (
    get_create_user_from_admin_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.post(
    "/create_user_from_admin",
    status_code=201,
    summary="Create User from Admin",
    description="Endpoint for creating a new user from admin. Returns a message indicating the result of the user creation.",
    tags=["User Management"],
    responses={
        201: {
            "description": "User created successfully. Returns a message indicating the successful creation.",
            "content": {
                "application/json": {
                    "example": {"message": "User created successfully."}
                }
            },
        },
        400: {
            "description": "Bad Request. User creation failed due to invalid input data.",
            "content": {
                "application/json": {
                    "example": {"message": "User creation failed. Invalid input data."}
                }
            },
        },
        401: {
            "description": "Unauthorized. User creation failed due to lack of authorization.",
            "content": {
                "application/json": {
                    "example": {"message": "User creation failed. Unauthorized."}
                }
            },
        },
        500: {
            "description": "Internal Server Error. User creation failed due to server error.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User creation failed. Internal server error."
                    }
                }
            },
        },
    },
)
async def create_user_from_admin(
    request: CreateUserFromAdminRequest,
    handler: Annotated[
        CreateUserFromAdminHandler, Depends(get_create_user_from_admin_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> CreateUserFromAdminResponse:
    """
    Endpoint for creating a new user from admin.

    Args:
        request (CreateUserFromAdminRequest): Request object containing the user data for creation.
        handler (CreateUserFromAdminHandler): Handler responsible for processing the user creation logic.

    Returns:
        CreateUserFromAdminResponse: Response object containing the result of the user creation process.
    """
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.message)
    return response
