from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)
from src.features.content_management.update_resource_status.update_resource_status_request import (
    UpdateResourceStatusRequest,
)
from src.features.content_management.update_resource_status.update_resource_status_response import (
    UpdateResourceStatusResponse,
)


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
                message="Status cannot be updated",
                content_id="",
                new_status=False,
            )
        return UpdateResourceStatusResponse(
            is_success=True,
            message="Resource content status has been updated",
            content_id=request.content_id,
            new_status=request.status,
        )
