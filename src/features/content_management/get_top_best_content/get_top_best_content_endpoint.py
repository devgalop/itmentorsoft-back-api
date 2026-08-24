from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_top_best_content.get_top_best_content_handler import (
    GetTopBestContentHandler,
)
from src.features.content_management.get_top_best_content.get_top_best_content_request import (
    GetTopBestContentRequest,
)
from src.features.content_management.get_top_best_content.get_top_best_content_response import (
    GetTopBestContentResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_top_best_content_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/top-content/best/{limit}",
    status_code=200,
    summary="Get top best content by topic",
    description="Endpoint to retrieve the top best educational resource contents based on rating for a specific topic.",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Top best content retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Top best content retrieved successfully.",
                        "items": [],
                    }
                }
            },
        },
        404: {
            "description": "Not Found. No top best content found for the given topic.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "No top best content found for the given topic.",
                        "items": [],
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error. An unexpected error occurred while processing the request.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "An unexpected error occurred while processing the request."
                    }
                }
            },
        },
    },
)
async def get_top_best_content(
    limit: int,
    topic: str,
    handler: Annotated[
        GetTopBestContentHandler, Depends(get_get_top_best_content_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher", "student"]))],
) -> GetTopBestContentResponse:
    """Get top best content by topic

    Args:
        limit (int): The maximum number of top best educational resource contents to retrieve.
        topic (str): The topic to filter the educational resource contents.
        handler (GetTopBestContentHandler): The handler for processing the request.
        _: TokenData: The token data for authentication and authorization.

    Returns:
        GetTopBestContentResponse: A response containing the top best educational resource contents based on rating for the specified topic.
    """
    try:
        request = GetTopBestContentRequest(topic=topic, limit=limit)
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
