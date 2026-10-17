from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_handler import (
    GetPendingApprovalQuestionsHandler,
)
from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_request import (
    GetPendingApprovalQuestionsRequest,
)
from src.features.assessments.shared.dependencies import (
    get_get_pending_approval_questions_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/pending-approval-questions",
    status_code=200,
    summary="Get all questions pending approval",
    description="Endpoint to retrieve all questions pending approval with pagination.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Pending approval questions retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Pending approval questions retrieved successfully.",
                        "questions": [
                            {
                                "question_id": "123e4567e89b12d3a456426614174000",
                                "text_to_evaluate": "Explain the difference between...",
                            }
                        ],
                        "total": 10,
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
async def get_pending_approval_questions(
    page: int,
    page_size: int,
    handler: Annotated[
        GetPendingApprovalQuestionsHandler,
        Depends(get_get_pending_approval_questions_handler),
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin"]))],
):
    request = GetPendingApprovalQuestionsRequest(page=page, page_size=page_size)
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
