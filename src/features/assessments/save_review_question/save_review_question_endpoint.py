from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.save_review_question.save_review_question_handler import (
    SaveReviewQuestionHandler,
)
from src.features.assessments.save_review_question.save_review_question_request import (
    SaveReviewQuestionRequest,
)
from src.features.assessments.save_review_question.save_review_question_response import (
    SaveReviewQuestionResponse,
)
from src.features.assessments.shared.dependencies import (
    get_save_review_question_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.post(
    "/review",
    status_code=200,
    summary="Save review for a question",
    description="Endpoint to save a review for a question.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Review saved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Review saved successfully",
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
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Internal server error.",
                    }
                }
            },
        },
    },
)
async def save_review_question(
    request: SaveReviewQuestionRequest,
    handler: Annotated[
        SaveReviewQuestionHandler, Depends(get_save_review_question_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
) -> SaveReviewQuestionResponse:
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.message)
    return response
