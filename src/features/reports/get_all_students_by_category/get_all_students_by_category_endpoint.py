from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.reports.get_all_students_by_category.get_all_students_by_category_handler import (
    GetStudentsByCategoryHandler,
)
from src.features.reports.get_all_students_by_category.get_all_students_by_category_request import (
    GetStudentsByCategoryRequest,
)
from src.features.reports.get_all_students_by_category.get_all_students_by_category_response import (
    GetStudentsByCategoryResponse,
)
from src.features.reports.shared.dependencies import (
    get_get_students_by_category_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData

router = APIRouter()


@router.get(
    "/students-by-category",
    status_code=200,
    summary="Get all students by category",
    description="Retrieve a paginated list of all students filtered by category.",
    tags=["Reports"],
    responses={
        200: {
            "description": "Students retrieved successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Students retrieved successfully",
                        "result": {
                            "students": [
                                {
                                    "student_id": "1",
                                    "student_name": "John Doe",
                                    "knowledge_classification": "Beginner",
                                }
                            ],
                            "total_students": 100,
                            "page": 1,
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
            "description": "Students not found.",
            "content": {
                "application/json": {
                    "example": {"is_success": False, "message": "Students not found."}
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
async def get_all_students_by_category(
    category: str,
    page: int,
    page_size: int,
    handler: Annotated[
        GetStudentsByCategoryHandler, Depends(get_get_students_by_category_handler)
    ],
    _: Annotated[TokenData, Depends(require_roles(["admin", "teacher"]))],
) -> GetStudentsByCategoryResponse:
    """
    Endpoint to retrieve a paginated list of all students filtered by category.

    - **category**: The category to filter students by.
    - **page**: The page number for pagination (0-indexed).
    - **page_size**: The number of students to return per page.

    Returns a response containing the list of students, total number of students, and the current page.
    """
    response = await handler.handle(
        GetStudentsByCategoryRequest(category=category, page=page, page_size=page_size)
    )
    if not response.is_success:
        raise HTTPException(status_code=400, detail=response.message)
    return response
