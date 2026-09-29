from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_handler import (
    GetAllQuestionsByVersionsHandler,
)
from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_request import (
    GetAllQuestionsByVersionsRequest,
)
from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_response import (
    GetAllQuestionsByVersionsResponse,
)
from src.features.assessments.shared.dependencies import (
    get_get_all_questions_by_versions_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/all-questions",
    status_code=200,
    summary="Retrieve all questions by their latest versions",
    description="Retrieve all questions by their latest versions",
    tags=["Assessments"],
    responses={
        200: {
            "description": "Successful response with the list of all questions by their latest versions",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Questions retrieved successfully",
                        "questions": [],
                        "total": 0,
                    }
                }
            },
        },
        404: {
            "description": "No questions found",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "No questions found",
                        "questions": [],
                        "total": 0,
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Unauthorized",
                        "questions": [],
                        "total": 0,
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
                        "questions": [],
                        "total": 0,
                    }
                }
            },
        },
    },
)
async def get_all_questions_by_versions(
    page: int,
    page_size: int,
    handler: Annotated[
        GetAllQuestionsByVersionsHandler,
        Depends(get_get_all_questions_by_versions_handler),
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> GetAllQuestionsByVersionsResponse:
    try:
        request = GetAllQuestionsByVersionsRequest(page=page, page_size=page_size)
        response = await handler.handle(request=request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
