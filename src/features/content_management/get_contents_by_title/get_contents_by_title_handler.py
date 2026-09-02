from src.features.content_management.get_contents_by_title.get_contents_by_title_request import (
    GetContentsByTitlePaginationRequest,
)
from itmentorsoft_persistence.dto import (
    GetContentsByTitlePaginationRequest as req,
)
from src.features.content_management.get_contents_by_title.get_contents_by_title_response import (
    GetContentsByTitleResponse,
)
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class GetContentsByTitleHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: GetContentsByTitlePaginationRequest
    ) -> GetContentsByTitleResponse:
        request_mapped = req(
            title=request.title, page=request.page, page_size=request.page_size
        )
        result = await self.content_repository.get_resource_contents_by_title(
            request_mapped
        )
        return GetContentsByTitleResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=result.items,
            total=result.total,
        )
