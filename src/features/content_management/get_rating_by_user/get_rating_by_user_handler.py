from itmentorsoft_persistence import ResourceContentRepository
from src.features.content_management.get_rating_by_user.get_rating_by_user_response import (
    RatingDetails,
)
from src.features.content_management.get_rating_by_user.get_rating_by_user_request import (
    GetContentRatingByUserRequest,
)
from src.features.content_management.get_rating_by_user.get_rating_by_user_response import (
    GetContentRatingByUserResponse,
)


class GetContentRatingByUserHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentRatingByUserRequest
    ) -> GetContentRatingByUserResponse:
        ratings = await self.content_repository.get_ratings_by_user(request.user_id)
        if not ratings:
            return GetContentRatingByUserResponse(
                is_success=False,
                message="No ratings found for the user.",
                rating_details=[],
            )
        result_ratings = [
            RatingDetails(
                content_id=rating.content_id,
                title=rating.title,
                summary=rating.summary,
                rating=rating.rating,
                student_id=rating.student_id,
            )
            for rating in ratings
        ]
        return GetContentRatingByUserResponse(
            is_success=True,
            message="Ratings retrieved successfully.",
            rating_details=result_ratings,
        )
