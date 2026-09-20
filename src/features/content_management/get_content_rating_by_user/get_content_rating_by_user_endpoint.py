from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_handler import (
    GetContentRatingByUserHandler,
)
from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_request import (
    GetContentRatingByUserRequest,
)
from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_response import (
    GetContentRatingByUserResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_content_rating_by_user_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData
from src.features.user_management.shared.validate_user import UserIdentityValidator

router = APIRouter()


@router.get(
    "/ratings/content",
    status_code=200,
    summary="Retrieve content rating by user",
    description="Retrieve the rating given by a specific user for a specific content",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Content rating retrieved successfully.",
            "content": {
                "application/json": {"example": {"is_success": True, "rating": 4}}
            },
        },
        404: {
            "description": "Content rating not found.",
            "content": {
                "application/json": {"example": {"is_success": False, "rating": None}}
            },
        },
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {"example": {"is_success": False, "rating": None}}
            },
        },
    },
)
async def get_content_rating_by_user(
    user_id: str,
    content_id: str,
    handler: Annotated[
        GetContentRatingByUserHandler, Depends(get_get_content_rating_by_user_handler)
    ],
    token_data: Annotated[TokenData, Depends(require_roles(["student"]))],
) -> GetContentRatingByUserResponse:
    try:
        request = GetContentRatingByUserRequest(user_id=user_id, content_id=content_id)
        UserIdentityValidator.is_valid_user(
            user_logged=token_data, user_id_to_validate=user_id
        )
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail="Content rating not found.")
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
