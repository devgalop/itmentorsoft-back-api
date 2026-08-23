from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from src.features.content_management.get_learning_path_progress.get_learning_path_progress_handler import (
    GetLearningPathProgressHandler,
)
from src.features.content_management.get_learning_path_progress.get_learning_path_progress_request import (
    GetLearningPathProgressRequest,
)
from src.features.content_management.get_learning_path_progress.get_learning_path_progress_response import (
    GetLearningPathProgressResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_learning_path_progress_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/learning-path/progress",
    status_code=200,
    summary="Get learning path progress",
    description="Endpoint to retrieve the progress of a learning path for a user.",
    tags=["Learning Path Management"],
    responses={
        200: {
            "description": "Learning path progress retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Learning path progress retrieved successfully.",
                        "path_progress": 0.75,
                    }
                }
            },
        },
        404: {
            "description": "Not Found. Learning path not found.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Learning path not found.",
                        "path_progress": None,
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error.",
            "content": {
                "application/json": {
                    "example": {"message": "An unexpected error occurred."}
                }
            },
        },
    },
)
async def get_learning_path_progress(
    path_id: str,
    handler: Annotated[
        GetLearningPathProgressHandler, Depends(get_get_learning_path_progress_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["student"]))],
) -> GetLearningPathProgressResponse:
    try:
        request = GetLearningPathProgressRequest(path_id=path_id)
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
