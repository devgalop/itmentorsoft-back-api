from src.i18n import t
from src.features.content_management.get_recommended_content.get_recommended_content_request import (
    GetRecommendedContentRequest,
)
from src.features.content_management.get_recommended_content.get_recommended_content_response import (
    GetRecommendedContentResponse,
)
from src.features.content_management.shared.learning_path_manager_service import (
    LearningPathManagerService,
)


class GetRecommendedContentHandler:
    def __init__(self, learning_path_service: LearningPathManagerService):
        self.learning_path_service = learning_path_service

    DEFAULT_ERROR_MESSAGE = t("content.learning_path.retrieval_failed")

    async def handle(
        self, request: GetRecommendedContentRequest
    ) -> GetRecommendedContentResponse:

        if not await self.learning_path_service.check_path_association(
            request.student_id, request.path_id
        ):
            return GetRecommendedContentResponse(
                is_success=False,
                message=self.DEFAULT_ERROR_MESSAGE,
                recommendation=None,
            )

        response = await self.learning_path_service.get_learning_path(request.path_id)

        if not response or not response.is_success:
            return GetRecommendedContentResponse(
                is_success=False,
                message=self.DEFAULT_ERROR_MESSAGE,
                recommendation=None,
            )

        return GetRecommendedContentResponse(
            is_success=True,
            message=t("content.learning_path.retrieved"),
            recommendation=response.learning_path,
        )
