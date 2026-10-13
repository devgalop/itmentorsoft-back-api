from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.features.content_management.get_complete_learning_path.get_complete_learning_path_request import (
    GetCompleteLearningPathRequest,
)
from src.features.content_management.get_complete_learning_path.get_complete_learning_path_handler import (
    GetCompleteLearningPathHandler,
)
from src.features.content_management.get_complete_learning_path.get_complete_learning_path_response import (
    GetCompleteLearningPathResponse,
)
from src.features.content_management.shared.dependencies import (
    get_get_complete_learning_path_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData
from src.features.user_management.shared.validate_user import UserIdentityValidator

router = APIRouter()


@router.get(
    "/complete/path",
    status_code=200,
    summary="Retrieve the complete learning path for the user",
    description="Retrieve the complete learning path for the user",
    tags=["Learning Path Management"],
    responses={
        200: {
            "description": "Successfully retrieved the complete learning path",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Successfully retrieved the complete learning path",
                        "data": {
                            "learning_path": [
                                {
                                    "id": "1",
                                    "title": "Introduction to Python",
                                    "description": "Learn the basics of Python programming",
                                }
                            ]
                        },
                    }
                }
            },
        },
        404: {
            "description": "Learning path not found",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Learning path not found",
                        "data": None,
                    }
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Internal server error",
                        "data": None,
                    }
                }
            },
        },
    },
)
async def get_complete_learning_path(
    user_id: str,
    handler: Annotated[
        GetCompleteLearningPathHandler, Depends(get_get_complete_learning_path_handler)
    ],
    token_data: Annotated[TokenData, Depends(require_roles(["student", "admin"]))],
    page: int = 0,
    page_size: int = 10,
) -> GetCompleteLearningPathResponse:

    try:
        request = GetCompleteLearningPathRequest(
            user_id=user_id, page=page, page_size=page_size
        )

        UserIdentityValidator.is_valid_user(
            user_logged=token_data, user_id_to_validate=user_id
        )

        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
