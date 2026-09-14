from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from src.features.assessments.shared.dependencies import get_update_question_handler
from src.features.assessments.update_question.update_question_handler import (
    UpdateQuestionHandler,
)
from src.features.assessments.update_question.update_question_request import (
    UpdateQuestionRequest,
)
from src.features.assessments.update_question.update_question_response import (
    UpdateQuestionResponse,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.put(
    "/questions/{question_id}",
    summary="Update a question",
    description="Endpoint to update an existing question with its rubric and related information.",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Question updated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Question updated successfully",
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
        404: {
            "description": "Question not found.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Question not found"}
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
async def update_question(
    question_id: Annotated[str, Path(description="The ID of the question to update")],
    request: UpdateQuestionRequest,
    handler: Annotated[UpdateQuestionHandler, Depends(get_update_question_handler)],
    token_data: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> UpdateQuestionResponse:
    response = await handler.handle(question_id, request, token_data.user_name)
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.model_dump())
    return response
