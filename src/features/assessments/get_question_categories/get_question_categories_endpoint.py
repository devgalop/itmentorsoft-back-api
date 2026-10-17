from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_question_categories.get_question_categories_handler import (
    GetQuestionCategoriesHandler,
)
from src.features.assessments.get_question_categories.get_question_categories_request import (
    GetQuestionCategoriesRequest,
)
from src.features.assessments.get_question_categories.get_question_categories_response import (
    GetQuestionCategoriesResponse,
)
from src.features.assessments.shared.dependencies import (
    get_get_question_categories_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/categories",
    status_code=200,
    summary="Get question categories",
    description="Endpoint to retrieve all question categories for a specific version.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Question categories retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Question categories retrieved successfully.",
                        "categories": ["Math", "Science", "History"],
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
        404: {
            "description": "Question categories not found.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Question categories not found.",
                    }
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
    },
)
async def get_question_categories(
    version: int,
    handler: Annotated[
        GetQuestionCategoriesHandler, Depends(get_get_question_categories_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["student", "teacher", "admin"]))],
) -> GetQuestionCategoriesResponse:
    request = GetQuestionCategoriesRequest(version=version)
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.model_dump())
    return response
