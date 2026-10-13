from src.i18n.messages import t
from src.features.content_management.get_complete_learning_path.get_complete_learning_path_response import (
    GetCompleteLearningPathResponse,
)
from src.features.content_management.get_complete_learning_path.get_complete_learning_path_request import (
    GetCompleteLearningPathRequest,
)
from src.features.content_management.shared.learning_path_manager_service import (
    LearningPathManagerService,
)


class GetCompleteLearningPathHandler:
    def __init__(self, learning_path_service: LearningPathManagerService):
        self.learning_path_service = learning_path_service

    async def handle(
        self, request: GetCompleteLearningPathRequest
    ) -> GetCompleteLearningPathResponse:

        learning_paths = await self.learning_path_service.get_complete_learning_path(
            user_id=request.user_id, page=request.page, page_size=request.page_size
        )

        if not learning_paths or not learning_paths.items:
            return GetCompleteLearningPathResponse(
                is_success=False,
                message=t("learning_path.not_found"),
                learning_path=None,
            )

        return GetCompleteLearningPathResponse(
            is_success=True,
            message=t("learning_path.retrieved"),
            learning_path=learning_paths.items,
        )
