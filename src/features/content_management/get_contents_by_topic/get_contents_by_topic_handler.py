from src.features.content_management.get_contents_by_topic.get_contents_by_topic_request import (
    GetContentsByTopicPaginationRequest,
)
from itmentorsoft_persistence.dto import (
    GetContentsByTopicPaginationRequest as req,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_response import (
    GetContentsByTopicResponse,
)
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class GetContentsByTopicHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentsByTopicPaginationRequest
    ) -> GetContentsByTopicResponse:

        request_mapped = req(
            topic=request.topic, page=request.page, page_size=request.page_size
        )
        result = await self.content_repository.get_resource_contents_by_related_topic(
            request_mapped
        )
        return GetContentsByTopicResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=result.items,
            total=result.total,
        )
