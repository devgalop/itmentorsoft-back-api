from src.features.content_management.get_top_best_content.get_top_best_content_request import (
    GetTopBestContentRequest,
)
from src.features.content_management.get_top_best_content.get_top_best_content_response import (
    GetTopBestContentResponse,
    TopBestContentItem,
)
from itmentorsoft_persistence.dto import TopContentOrder
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class GetTopBestContentHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetTopBestContentRequest
    ) -> GetTopBestContentResponse:
        top_content = await self.content_repository.get_top_content(
            topic=request.topic,
            limit=request.limit,
            order=TopContentOrder.DESCENDING.value,
        )
        if not top_content:
            return GetTopBestContentResponse(
                is_success=False,
                message="No top best content found for the given topic.",
                items=[],
            )

        items = [
            TopBestContentItem(
                content_id=content.content_id,
                title=content.title,
                summary=content.summary,
                rating=content.rating,
            )
            for content in top_content
        ]
        return GetTopBestContentResponse(
            is_success=True,
            message="Top best content retrieved successfully.",
            items=items,
        )
