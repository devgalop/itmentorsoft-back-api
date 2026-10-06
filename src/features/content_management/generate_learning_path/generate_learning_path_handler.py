from src.i18n.messages import t
from src.features.content_management.shared.learning_path_manager_service import (
    LearningPathManagerService,
)
from src.features.content_management.generate_learning_path.generate_learning_path_request import (
    GenerateLearningPathRequest,
)
from src.features.content_management.generate_learning_path.generate_learning_path_response import (
    GenerateLearningPathResponse,
)


class GenerateLearningPathHandler:
    def __init__(self, learning_path_service: LearningPathManagerService):
        self.learning_path_service = learning_path_service

    async def handle(
        self, request: GenerateLearningPathRequest
    ) -> GenerateLearningPathResponse:
        learning_path_response = await self.learning_path_service.create_learning_path(
            request.student_id
        )
        if not learning_path_response.is_success:
            return GenerateLearningPathResponse(
                is_success=False,
                message=learning_path_response.message,
                learning_path=None,
            )

        learning_path = learning_path_response.topic_paths

        return GenerateLearningPathResponse(
            is_success=True,
            message=t("learning_path.created"),
            learning_path=learning_path,
        )
