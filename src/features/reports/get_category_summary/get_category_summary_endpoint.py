from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.reports.get_category_summary.get_category_summary_handler import (
    GetCategorySummaryHandler,
)
from src.features.reports.get_category_summary.get_category_summary_request import (
    GetCategorySummaryRequest,
)
from src.features.reports.get_category_summary.get_category_summary_response import (
    GetCategorySummaryResponse,
)
from src.features.reports.shared.dependencies import get_get_category_summary_handler
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData
from src.i18n import t

router = APIRouter()


@router.get(
    "/category_summary",
    status_code=200,
    summary="Get category summary",
    description="Retrieve the summary of a specific category.",
    tags=["Reports"],
    responses={
        200: {
            "description": "Category summary retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Category summary retrieved successfully",
                        "category_summary": {
                            "category": "Mathematics",
                            "total_students": 150,
                        },
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
            "description": "Category summary not found.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Category summary not found",
                    }
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
async def get_category_summary(
    category: str,
    handler: Annotated[
        GetCategorySummaryHandler, Depends(get_get_category_summary_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> GetCategorySummaryResponse:
    if not category:
        raise HTTPException(status_code=400, detail=t("validation.category.required"))
    try:
        request = GetCategorySummaryRequest(category=category)
        response = await handler.handle(request)
        if not response.is_success:
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
