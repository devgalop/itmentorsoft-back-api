from src.features.assessments.get_qualification_status.get_qualification_status_request import (
    GetQualificationStatusRequest,
)
from src.features.assessments.get_qualification_status.get_qualification_status_response import (
    GetQualificationStatusResponse,
)
from itmentorsoft_persistence.repositories import AssessmentRepository


class GetQualificationStatusHandler:
    def __init__(self, assessment_repository: AssessmentRepository):
        self.assessment_repository = assessment_repository

    async def handle(
        self, request: GetQualificationStatusRequest
    ) -> GetQualificationStatusResponse:
        is_completed = await self.assessment_repository.is_qualification_completed(
            request.user_id, request.assessment_id
        )
        return GetQualificationStatusResponse(is_already_qualified=is_completed)
