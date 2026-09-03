from typing import Type

from src.features.content_management.register_content.register_content_request import (
    RegisterContentRequest,
)
from itmentorsoft_persistence.dto import (
    GetContentsByTitlePaginationRequest as GetContentsByTitlePaginationRequestDTO,
)
from src.features.content_management.register_content.register_content_response import (
    RegisterContentResponse,
)
from itmentorsoft_persistence.dto import (
    ContentCategory,
    ResourceContent,
    ResourceContentBuilder,
)
from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)


class RegisterContentHandler:

    def __init__(
        self,
        content_repository: ResourceContentRepository,
        content_builder: Type[ResourceContentBuilder],
    ):
        self.content_repository = content_repository
        self.content_builder = content_builder

    async def handle(self, request: RegisterContentRequest) -> RegisterContentResponse:

        content = await self.content_repository.get_resource_contents_by_title(
            GetContentsByTitlePaginationRequestDTO(
                title=request.title, page=0, page_size=1
            )
        )
        if content.total > 0:
            return RegisterContentResponse(
                is_success=False,
                content_id=None,
                message="Content with the same title already exists",
            )

        if not request.category:
            # Default category is NOVICE if not provided
            request.category = ContentCategory.NOVICE.value

        valid_categories = [category.value for category in ContentCategory]
        if request.category not in valid_categories:
            return RegisterContentResponse(
                is_success=False, content_id=None, message="Invalid category provided"
            )

        if not request.related_topic:
            # Default related topic is empty list if not provided
            request.related_topic = []

        content_build: ResourceContent = (
            self.content_builder()
            .set_title(request.title)
            .set_summary(request.description)
            .set_url(request.url)
            .set_category(ContentCategory(request.category))
            .add_related_topics(request.related_topic)
            .build()
        )
        await self.content_repository.save(content_build)

        return RegisterContentResponse(
            is_success=True,
            content_id=content_build.content_id,
            message="Content registered successfully",
        )
