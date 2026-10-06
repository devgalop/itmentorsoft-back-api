from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.features.content_management.generate_learning_path.generate_learning_path_handler import (
    GenerateLearningPathHandler,
)
from src.features.content_management.generate_learning_path.generate_learning_path_request import (
    GenerateLearningPathRequest,
)
from src.features.content_management.generate_learning_path.generate_learning_path_response import (
    GenerateLearningPathResponse,
)
from src.features.content_management.shared.dependencies import (
    get_generate_learning_path_handler,
)
from src.features.user_management.shared.require_roles import require_roles
from src.features.user_management.shared.token_generator import TokenData
from src.features.user_management.shared.validate_user import UserIdentityValidator

router = APIRouter()


@router.post(
    "/generate/learning-path",
    status_code=200,
    summary="Generate a learning path for the student",
    description="Endpoint to generate a learning path for a student",
    tags=["Learning Path Management"],
    responses={
        200: {
            "description": "Learning path successfully generated",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": True,
                        "message": "Learning path successfully generated",
                        "learning_path": {
                            "id": "123",
                            "name": "Sample Learning Path",
                            "courses": [{"id": "course_1", "name": "Course 1"}],
                        },
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Bad Request",
                        "learning_path": None,
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
                        "learning_path": None,
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "is_success": False,
                        "message": "Internal Server Error",
                        "learning_path": None,
                    }
                }
            },
        },
    },
)
async def generate_learning_path(
    student_id: str,
    handler: Annotated[
        GenerateLearningPathHandler, Depends(get_generate_learning_path_handler)
    ],
    token_data: Annotated[TokenData, Depends(require_roles(["student"]))],
) -> GenerateLearningPathResponse:

    try:
        request = GenerateLearningPathRequest(student_id=student_id)

        UserIdentityValidator.is_valid_user(
            user_logged=token_data, user_id_to_validate=student_id
        )

        response = await handler.handle(request=request)

        if not response.is_success:
            raise HTTPException(status_code=400, detail=response.message)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
