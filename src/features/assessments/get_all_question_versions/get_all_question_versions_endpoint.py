from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.assessments.get_all_question_versions.get_all_question_versions_handler import (
    GetAllQuestionVersionsHandler,
)
from src.features.assessments.get_all_question_versions.get_all_question_versions_request import (
    GetAllQuestionVersionsRequest,
)
from src.features.assessments.get_all_question_versions.get_all_question_versions_response import (
    GetAllQuestionVersionsResponse,
)
from src.features.assessments.shared.dependencies import (
    get_get_all_question_versions_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/question-versions",
    status_code=200,
    summary="Retrieve all versions of a specific question.",
    description="Retrieve all versions of a specific question by its ID.",
    tags=["Assessments"],
    responses={
        200: {"description": "Successfully retrieved all question versions."},
        404: {"description": "No question versions found."},
        401: {"description": "Unauthorized access."},
    },
)
async def get_all_question_versions(
    question_id: str,
    handler: Annotated[
        GetAllQuestionVersionsHandler, Depends(get_get_all_question_versions_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["teacher", "admin"]))],
) -> GetAllQuestionVersionsResponse:

    try:
        request = GetAllQuestionVersionsRequest(question_id=question_id)
        response = await handler.handle(request=request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
