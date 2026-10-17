from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.shared.dependencies import (
    get_update_question_status_handler,
)
from src.features.assessments.update_question_status.update_question_status_handler import (
    UpdateQuestionStatusHandler,
)
from src.features.assessments.update_question_status.update_question_status_request import (
    UpdateQuestionStatusRequest,
)
from src.features.assessments.update_question_status.update_question_status_response import (
    UpdateQuestionStatusResponse,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.put(
    "/question/update/status",
    status_code=200,
    summary="Update the status of a question",
    description="Update the status of a question by providing its ID and the new status.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Question status updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Question status updated successfully",
                        "question_id": "12345",
                        "new_status": True,
                    }
                }
            },
        },
        404: {
            "description": "Question not found",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Question with ID 12345 not found",
                        "question_id": "",
                        "new_status": False,
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
                        "message": "An unexpected error occurred while updating the question status.",
                        "question_id": "",
                        "new_status": False,
                    }
                }
            },
        },
    },
)
async def update_question_status(
    request: UpdateQuestionStatusRequest,
    handler: Annotated[
        UpdateQuestionStatusHandler, Depends(get_update_question_status_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> UpdateQuestionStatusResponse:
    response = await handler.handle(request)
    if not response.is_success:
        raise HTTPException(status_code=404, detail=response.message)
    return response
