from src.i18n import t
from src.features.assessments.get_assessment.get_assessment_request import (
    GetAssessmentRequest,
)
from src.features.assessments.get_assessment.get_assessment_response import (
    GetAssessmentResponse,
)
from src.features.assessments.shared.get_assessment_service import (
    GetAssessmentService,
)


class GetAssessmentHandler:
    def __init__(self, get_assessment_service: GetAssessmentService):
        self.get_assessment_service = get_assessment_service

    async def handle(self, request: GetAssessmentRequest) -> GetAssessmentResponse:
        try:
            response = await self.get_assessment_service.generate_assessment(request)
            return response
        except Exception as e:
            return GetAssessmentResponse(
                is_success=False,
                message=t("assessment.retrieval_failed", error=str(e)),
                assessment_id=None,
                questions=None,
            )
