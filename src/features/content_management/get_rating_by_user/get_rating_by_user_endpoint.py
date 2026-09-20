from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_rating_by_user.get_rating_by_user_handler import (
    GetContentRatingByUserHandler,
)
from src.features.content_management.get_rating_by_user.get_rating_by_user_request import (
    GetContentRatingByUserRequest,
)
from src.features.content_management.shared.dependencies import (
    get_get_rating_by_user_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData
from src.features.content_management.get_rating_by_user.get_rating_by_user_response import (
    GetContentRatingByUserResponse,
)
from src.features.user_management.shared.validate_user import UserIdentityValidator

router = APIRouter()


@router.get(
    "/ratings/all",
    status_code=200,
    summary="Get all ratings applied by a specific user",
    description="Retrieve all ratings applied by a specific user",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Ratings retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Ratings retrieved successfully.",
                        "rating_details": [
                            {
                                "content_id": "content123",
                                "title": "Sample Content",
                                "summary": "This is a sample content summary.",
                                "rating": 5,
                                "student_id": "student123",
                            }
                        ],
                    }
                }
            },
        },
        404: {
            "description": "No ratings found for the user.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "No ratings found for the user.",
                        "rating_details": [],
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized access.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Unauthorized access.",
                        "rating_details": [],
                    }
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
                        "rating_details": [],
                    }
                }
            },
        },
    },
)
async def get_ratings_by_user(
    user_id: str,
    handler: Annotated[
        GetContentRatingByUserHandler, Depends(get_get_rating_by_user_handler)
    ],
    token_data: Annotated[TokenData, Depends(require_roles(["student"]))],
) -> GetContentRatingByUserResponse:
    try:
        request = GetContentRatingByUserRequest(user_id=user_id)
        UserIdentityValidator.is_valid_user(
            user_logged=token_data, user_id_to_validate=user_id
        )
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
