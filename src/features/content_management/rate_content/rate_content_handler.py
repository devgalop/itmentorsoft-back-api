import uuid

from src.features.content_management.rate_content.rate_content_request import (
    RateContentRequest,
)
from itmentorsoft_persistence.dto import RateContent as RateContentDTO
from src.features.content_management.rate_content.rate_content_response import (
    RateContentResponse,
)
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)
from src.i18n import t


class RateContentHandler:
    def __init__(self, resource_content_repository: ResourceContentRepository):
        self.resource_content_repository = resource_content_repository

    async def handle(self, request: RateContentRequest) -> RateContentResponse:
        content_found = await self.resource_content_repository.get_resource_content(
            request.content_id
        )
        if not content_found:
            return RateContentResponse(
                is_success=False,
                message=t("content.not_found", content_id=request.content_id),
            )
        rate_content = RateContentDTO(
            id=uuid.uuid4().hex,
            content_id=request.content_id,
            user_id=request.user_id,
            rating=request.rating,
            comment=request.comment,
        )
        await self.resource_content_repository.rate_resource_content(rate_content)
        return RateContentResponse(is_success=True, message=t("content.rated"))
