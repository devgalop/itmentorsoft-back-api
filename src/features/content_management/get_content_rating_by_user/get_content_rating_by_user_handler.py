from itmentorsoft_persistence import ResourceContentRepository

from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_request import (
    GetContentRatingByUserRequest,
)
from src.features.content_management.get_content_rating_by_user.get_content_rating_by_user_response import (
    GetContentRatingByUserResponse,
    RatingDetail,
)


class GetContentRatingByUserHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentRatingByUserRequest
    ) -> GetContentRatingByUserResponse:
        rating = await self.content_repository.get_rating_content_by_user(
            request.user_id, request.content_id
        )
        if rating is None:
            return GetContentRatingByUserResponse(
                is_success=False, message="Rating not found", rating_detail=None
            )

        rating_detail = RatingDetail(
            content_id=rating.content_id,
            title=rating.title,
            summary=rating.summary,
            rating=rating.rating,
            student_id=rating.student_id,
        )
        return GetContentRatingByUserResponse(
            is_success=True,
            message="Rating retrieved successfully",
            rating_detail=rating_detail,
        )
