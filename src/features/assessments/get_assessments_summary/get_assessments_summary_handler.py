from src.features.assessments.get_assessments_summary.get_assessments_summary_request import (
    GetAssessmentsSummaryRequest,
)
from src.features.assessments.get_assessments_summary.get_assessments_summary_response import (
    AssessmentSummary,
    GetAssessmentsSummaryResponse,
)
from itmentorsoft_persistence.repositories import AssessmentRepository


class GetAssessmentsSummaryHandler:
    def __init__(self, assessment_repository: AssessmentRepository):
        self.assessment_repository = assessment_repository

    async def handle(
        self, request: GetAssessmentsSummaryRequest
    ) -> GetAssessmentsSummaryResponse:

        response = await self.assessment_repository.get_assessments_summary(
            request.student_id, request.page, request.page_size
        )

        if response.total_assessments == 0:
            return GetAssessmentsSummaryResponse(
                is_success=False,
                message="No assessments found for the student.",
                total_assessments=0,
                assessments=[],
            )

        assessment_summaries = [
            AssessmentSummary(
                assessment_id=summary.assessment_id,
                score=summary.score,
                date_taken=summary.date_taken,
                classification=summary.classification,
                feedback=summary.feedback,
            )
            for summary in response.assessments
        ]

        return GetAssessmentsSummaryResponse(
            is_success=True,
            message="Assessments summary retrieved successfully.",
            total_assessments=response.total_assessments,
            assessments=assessment_summaries,
        )
