from itmentorsoft_persistence.dto import ContentCategory
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)
from src.features.content_management.update_resource_content.update_resource_content_request import (
    UpdateResourceContentRequest,
)
from itmentorsoft_persistence.dto import (
    UpdateResourceContentRequest as UpdateResourceContentRequestDTO,
)
from src.features.content_management.update_resource_content.update_resource_content_response import (
    UpdateResourceContentResponse,
)


class UpdateResourceContentHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, content_id: str, request: UpdateResourceContentRequest
    ) -> UpdateResourceContentResponse:
        try:
            if not request.category:
                request.category = ContentCategory.NOVICE.value

            valid_categories = [category.value for category in ContentCategory]
            if request.category not in valid_categories:
                return UpdateResourceContentResponse(
                    is_success=False, message="Invalid category provided"
                )

            if not request.related_topic:
                request.related_topic = []

            request_dto = UpdateResourceContentRequestDTO(
                title=request.title,
                description=request.description,
                url=request.url,
                category=request.category,
                related_topic=request.related_topic,
            )

            await self.content_repository.update_resource_content(
                content_id, request_dto
            )

            return UpdateResourceContentResponse(
                is_success=True,
                message=f"Content with ID {content_id} has been successfully updated.",
            )
        except ValueError as e:
            return UpdateResourceContentResponse(is_success=False, message=str(e))
