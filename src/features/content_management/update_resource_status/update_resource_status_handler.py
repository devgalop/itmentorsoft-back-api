from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)
from src.features.content_management.update_resource_status.update_resource_status_request import (
    UpdateResourceStatusRequest,
)
from src.features.content_management.update_resource_status.update_resource_status_response import (
    UpdateResourceStatusResponse,
)
from src.i18n import t


class UpdateResourceStatusHandler:
    def __init__(self, content_repository: ResourceContentRepository):
        self.content_repository = content_repository

    async def handle(
        self, request: UpdateResourceStatusRequest
    ) -> UpdateResourceStatusResponse:
        result = await self.content_repository.update_resource_status(
            content_id=request.content_id, new_status=request.status
        )
        if not result:
            return UpdateResourceStatusResponse(
                is_success=False,
                message=t("content.status.cannot_update"),
                content_id="",
                new_status=False,
            )
        return UpdateResourceStatusResponse(
            is_success=True,
            message=t("content.status.updated"),
            content_id=request.content_id,
            new_status=request.status,
        )
