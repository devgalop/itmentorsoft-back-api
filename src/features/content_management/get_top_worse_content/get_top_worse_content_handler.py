from src.features.content_management.get_top_worse_content.get_top_worse_content_request import (
    GetTopWorseContentRequest,
)
from src.features.content_management.get_top_worse_content.get_top_worse_content_response import (
    GetTopWorseContentResponse,
    TopWorseContentItem,
)
from itmentorsoft_persistence.dto import TopContentOrder
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class GetTopWorseContentHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetTopWorseContentRequest
    ) -> GetTopWorseContentResponse:
        top_content = await self.content_repository.get_top_content(
            topic=request.topic,
            limit=request.limit,
            order=TopContentOrder.ASCENDING.value,
        )
        if not top_content:
            return GetTopWorseContentResponse(
                is_success=False,
                message="No top worse content found for the given topic.",
                items=[],
            )

        items = [
            TopWorseContentItem(
                content_id=content.content_id,
                title=content.title,
                summary=content.summary,
                rating=content.rating,
            )
            for content in top_content
        ]
        return GetTopWorseContentResponse(
            is_success=True,
            message="Top worse content retrieved successfully.",
            items=items,
        )
