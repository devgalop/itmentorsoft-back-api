from src.features.content_management.get_contents_by_category.get_contents_by_category_request import (
    GetContentsByCategoryPaginationRequest as req,
)
from itmentorsoft_persistence.dto import (
    GetContentsByCategoryPaginationRequest,
)
from src.features.content_management.get_contents_by_category.get_contents_by_category_response import (
    GetContentsByCategoryResponse,
)
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class GetContentsByCategoryHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(self, request: req) -> GetContentsByCategoryResponse:
        request_mapped = GetContentsByCategoryPaginationRequest(
            category=request.category, page=request.page, page_size=request.page_size
        )
        response = await self.content_repository.get_resource_contents_by_category(
            request_mapped
        )

        return GetContentsByCategoryResponse(
            is_success=True,
            message="Contents retrieved successfully",
            items=response.items,
            total=response.total,
        )
