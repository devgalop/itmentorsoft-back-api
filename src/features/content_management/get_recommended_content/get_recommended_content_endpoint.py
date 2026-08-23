from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.content_management.get_recommended_content.get_recommended_content_handler import (
    GetRecommendedContentHandler,
)
from src.features.content_management.get_recommended_content.get_recommended_content_request import (
    GetRecommendedContentRequest,
)
from src.features.content_management.get_recommended_content.get_recommended_content_response import (
    GetRecommendedContentResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_recommended_content_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/recommended/learning-paths",
    status_code=200,
    summary="Get recommended content for a student",
    description="Retrieve recommended content for a student based on their learning path.",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Recommended content retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Learning paths retrieved successfully.",
                        "recommendation": [],
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Failed to retrieve learning paths.",
                        "recommendation": [],
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"detail": "An unexpected error occurred."}
                }
            },
        },
    },
)
async def get_recommended_content(
    user_id: str,
    handler: Annotated[
        GetRecommendedContentHandler, Depends(get_get_recommended_content_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["student"]))],
) -> GetRecommendedContentResponse:
    try:
        request = GetRecommendedContentRequest(student_id=user_id)
        response = await handler.handle(request)

        if not response.is_success:
            raise HTTPException(status_code=400, detail=response.message)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
