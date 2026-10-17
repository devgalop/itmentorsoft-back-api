from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_all_questions.get_all_questions_handler import (
    GetAllQuestionsHandler,
)
from src.features.assessments.get_all_questions.get_all_questions_request import (
    GetAllQuestionsRequest,
)
from src.features.assessments.get_all_questions.get_all_questions_response import (
    GetAllQuestionsResponse,
)
from src.features.assessments.shared.dependencies import get_get_all_questions_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/questions",
    status_code=200,
    summary="Get all questions paginated",
    description="Endpoint to retrieve all questions with pagination.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Questions retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Questions retrieved successfully",
                        "questions": [
                            {
                                "question_id": "123e4567e89b12d3a456426614174000",
                                "text_to_evaluate": "Explain the difference between...",
                            }
                        ],
                        "total": 100,
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
async def get_all_questions(
    page: int,
    page_size: int,
    handler: Annotated[GetAllQuestionsHandler, Depends(get_get_all_questions_handler)],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> GetAllQuestionsResponse:
    request = GetAllQuestionsRequest(page=page, page_size=page_size)
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
