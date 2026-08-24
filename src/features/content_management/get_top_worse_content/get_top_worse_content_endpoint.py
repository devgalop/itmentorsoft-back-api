from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_top_worse_content.get_top_worse_content_handler import (
    GetTopWorseContentHandler,
)
from src.features.content_management.get_top_worse_content.get_top_worse_content_request import (
    GetTopWorseContentRequest,
)
from src.features.content_management.get_top_worse_content.get_top_worse_content_response import (
    GetTopWorseContentResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_top_worse_content_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/top-content/worse/{limit}",
    status_code=200,
    summary="Get top worse content by topic",
    description="Endpoint to retrieve the top worse educational resource contents based on rating for a specific topic.",
    tags=["Content Management"],
    responses={
        200: {
            "description": "Top worse content retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Top worse content retrieved successfully.",
                        "items": [],
                    }
                }
            },
        },
        404: {
            "description": "Not Found. No top worse content found for the given topic.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "No top worse content found for the given topic.",
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
async def get_top_worse_content(
    limit: int,
    topic: str,
    handler: Annotated[
        GetTopWorseContentHandler, Depends(get_get_top_worse_content_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher", "student"]))],
) -> GetTopWorseContentResponse:
    """Endpoint to retrieve the top worse educational resource contents based on rating for a specific topic.

    Args:
        limit (int): The maximum number of top worse educational resource contents to retrieve.
        topic (str): The topic to filter the educational resource contents.
        handler (GetTopWorseContentHandler): The handler responsible for processing the request.
        _ (TokenData): The token data containing user information and roles.

    Returns:
        GetTopWorseContentResponse: The response containing the top worse educational resource contents based on rating for the specified topic.
    """
    try:
        request = GetTopWorseContentRequest(topic=topic, limit=limit)
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
