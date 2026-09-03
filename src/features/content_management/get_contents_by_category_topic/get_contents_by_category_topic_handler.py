from src.features.content_management.get_contents_by_category_topic.get_contents_by_category_topic_request import (
    GetContentsByCategoryTopicPaginationRequest,
)
from itmentorsoft_persistence.dto import (
    GetContentsByCategoryTopicPaginationRequest as req,
)
from src.features.content_management.get_contents_by_category_topic.get_contents_by_category_topic_response import (
    GetContentsByCategoryTopicResponse,
)
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class GetContentsByCategoryTopicHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentsByCategoryTopicPaginationRequest
    ) -> GetContentsByCategoryTopicResponse:

        request_mapped = req(
            category=request.category,
            topic=request.topic,
            page=request.page,
            page_size=request.page_size,
        )
        result = await self.content_repository.get_resource_contents_by_category_and_related_topic(
            request_mapped
        )
        return GetContentsByCategoryTopicResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=result.items,
            total=result.total,
        )
