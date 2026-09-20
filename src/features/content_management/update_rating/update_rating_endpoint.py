from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.shared.dependencies import (
    get_update_rating_handler,
)
from src.features.content_management.update_rating.update_rating_handler import (
    UpdateRatingHandler,
)
from src.features.content_management.update_rating.update_rating_request import (
    UpdateRatingRequest,
)
from src.features.content_management.update_rating.update_rating_response import (
    UpdateRatingResponse,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData
from src.features.user_management.shared.validate_user import UserIdentityValidator

router = APIRouter()


@router.put(
    "/modify/rating",
    status_code=200,
    summary="Update a rating for a content item",
    description="Update the rating for a specific content item",
    responses={
        200: {
            "description": "Rating updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Rating updated successfully",
                    }
                }
            },
        },
        404: {
            "description": "Rating not found",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Rating not found"}
                }
            },
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Unauthorized"}
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Internal Server Error"}
                }
            },
        },
    },
)
async def update_rating(
    request: UpdateRatingRequest,
    handler: Annotated[UpdateRatingHandler, Depends(get_update_rating_handler)],
    token_data: Annotated[TokenData, Depends(require_roles(["student"]))],
) -> UpdateRatingResponse:
    try:
        UserIdentityValidator.is_valid_user(
            user_logged=token_data, user_id_to_validate=request.user_id
        )
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
