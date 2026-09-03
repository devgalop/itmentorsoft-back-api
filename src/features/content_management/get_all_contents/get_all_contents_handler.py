from src.features.content_management.get_all_contents.get_all_contents_request import (
    GetAllContentsRequest,
)
from src.features.content_management.get_all_contents.get_all_contents_response import (
    GetAllContentsResponse,
)
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class GetAllContentsHandler:

    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(self, request: GetAllContentsRequest) -> GetAllContentsResponse:
        result = await self.content_repository.get_all_resource_contents(
            request.page, request.page_size
        )
        return GetAllContentsResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=result.items,
            total=result.total,
        )
