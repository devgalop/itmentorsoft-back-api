from itmentorsoft_persistence.repositories import (
    LearningPathRepository,
)
from src.features.content_management.update_content_path_status.update_content_path_status_request import (
    UpdateContentPathStatusRequest,
)
from src.features.content_management.update_content_path_status.update_content_path_status_response import (
    UpdateContentPathStatusResponse,
)


class UpdateContentPathStatusHandler:
    def __init__(self, learning_path_repository: LearningPathRepository):
        self.learning_path_repository = learning_path_repository

    async def handle(
        self, request: UpdateContentPathStatusRequest
    ) -> UpdateContentPathStatusResponse:
        response = await self.learning_path_repository.update_status_content_path(
            request.path_id, request.content_id, request.status
        )

        if not response.is_success:
            return UpdateContentPathStatusResponse(
                is_success=response.is_success,
                message=response.message,
                path_progress=0.0,
            )

        return UpdateContentPathStatusResponse(
            is_success=response.is_success,
            message=response.message,
            path_progress=(
                response.path_progress.progress if response.path_progress else 0.0
            ),
        )
