from src.features.content_management.get_learning_path_progress.get_learning_path_progress_request import (
    GetLearningPathProgressRequest,
)
from src.features.content_management.get_learning_path_progress.get_learning_path_progress_response import (
    GetLearningPathProgressResponse,
)
from src.features.content_management.shared.learning_path_repository import (
    LearningPathRepository,
)


class GetLearningPathProgressHandler:
    def __init__(self, learning_path_repository: LearningPathRepository):
        self.learning_path_repository = learning_path_repository

    async def handle(
        self, request: GetLearningPathProgressRequest
    ) -> GetLearningPathProgressResponse:
        progress_response = (
            await self.learning_path_repository.get_learning_path_progress(
                request.path_id
            )
        )
        if not progress_response.is_success:
            return GetLearningPathProgressResponse(
                is_success=False, message=progress_response.message, path_progress=0.0
            )
        return GetLearningPathProgressResponse(
            is_success=True,
            message=progress_response.message,
            path_progress=(
                progress_response.path_progress.progress
                if progress_response.path_progress
                else 0.0
            ),
        )
