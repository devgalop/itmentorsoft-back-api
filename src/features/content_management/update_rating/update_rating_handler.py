from itmentorsoft_persistence import RateContent, ResourceContentRepository

from src.features.content_management.update_rating.update_rating_request import (
    UpdateRatingRequest,
)
from src.features.content_management.update_rating.update_rating_response import (
    UpdateRatingResponse,
)


class UpdateRatingHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(self, request: UpdateRatingRequest) -> UpdateRatingResponse:
        rating_found = await self.content_repository.get_rating_content_by_user(
            request.user_id, request.content_id
        )
        if not rating_found:
            return UpdateRatingResponse(is_success=False, message="Rating not found")

        await self.content_repository.update_rating(
            RateContent(
                id="",
                user_id=request.user_id,
                content_id=request.content_id,
                rating=request.rating,
                comment=request.comment,
            )
        )
        return UpdateRatingResponse(
            is_success=True, message="Rating updated successfully"
        )
