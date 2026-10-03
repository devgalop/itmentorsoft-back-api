from src.i18n import t
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_request import (
    GetAssessmentByTopicRequest,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_response import (
    GetAssessmentByTopicResponse,
)
from src.features.assessments.shared.get_assessment_service import GetAssessmentService


class GetAssessmentByTopicHandler:
    def __init__(self, get_assessment_service: GetAssessmentService):
        self.get_assessment_service = get_assessment_service

    async def handle(
        self, request: GetAssessmentByTopicRequest
    ) -> GetAssessmentByTopicResponse:
        try:
            response = await self.get_assessment_service.generate_assessment_by_topic(
                request
            )
            return response
        except Exception as e:
            return GetAssessmentByTopicResponse(
                is_success=False,
                message=t("assessment.retrieval_failed", error=str(e)),
                assessment_id=None,
                questions=None,
            )
