from src.features.content_management.get_recommended_content.get_recommended_content_request import (
    GetRecommendedContentRequest,
)
from src.features.content_management.get_recommended_content.get_recommended_content_response import (
    ContentByTopic,
    GetRecommendedContentResponse,
    TopicSummary,
)
from itmentorsoft_persistence.repositories import (
    LearningPathRepository,
)


class GetRecommendedContentHandler:
    def __init__(self, learning_path_repository: LearningPathRepository):
        self.learning_path_repository = learning_path_repository

    async def handle(
        self, request: GetRecommendedContentRequest
    ) -> GetRecommendedContentResponse:

        response = await self.learning_path_repository.get_learning_path(
            request.student_id
        )

        if not response.is_success:
            return GetRecommendedContentResponse(
                is_success=False,
                message="Failed to retrieve learning paths.",
                recommendation=[],
            )

        for learning_path in response.recommendation:
            await self.learning_path_repository.save_learning_path(learning_path)

        results = [
            TopicSummary(
                topic=learning_path.topic,
                contents=[
                    ContentByTopic(
                        content_id=content.content_id,
                        title=content.title,
                        description=content.description,
                        rating=content.rating,
                    )
                    for content in learning_path.contents
                ],
            )
            for learning_path in response.recommendation
        ]

        return GetRecommendedContentResponse(
            is_success=True,
            message="Learning paths retrieved successfully.",
            recommendation=results,
        )
