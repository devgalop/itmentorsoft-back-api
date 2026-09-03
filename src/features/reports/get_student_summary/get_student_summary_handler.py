from src.features.reports.get_student_summary.get_student_summary_request import (
    GetStudentSummaryRequest,
)
from src.features.reports.get_student_summary.get_student_summary_response import (
    GetStudentSummaryResponse,
    KnowledgeProfile,
    SummaryResponse,
)
from itmentorsoft_persistence.dto import StudentSummary
from src.features.reports.shared.student_report_service import StudentReportService


class GetStudentSummaryHandler:
    def __init__(self, student_report_service: StudentReportService):
        self.student_report_service = student_report_service

    async def handle(
        self, request: GetStudentSummaryRequest
    ) -> GetStudentSummaryResponse:
        """Handle the request to get the student summary by user ID.

        Args:
            request (GetStudentSummaryRequest): The request object containing the user ID.

        Returns:
            GetStudentSummaryResponse: The student summary corresponding to the given user ID.
        """
        response = await self.student_report_service.get_student_summary(
            request.student_id
        )
        if not response.is_success or not response.student_summary:
            return GetStudentSummaryResponse(
                is_success=False, message=response.message, summary=None
            )

        summary = self.map_to_response(response.student_summary)
        return GetStudentSummaryResponse(
            is_success=True, message=response.message, summary=summary
        )

    def map_to_response(self, student_summary: StudentSummary) -> SummaryResponse:
        """Map the student summary to the response model.

        Args:
            student_summary (StudentSummary): The student summary to be mapped.

        Returns:
            SummaryResponse: The mapped response model.
        """
        knowledge_profiles: list[KnowledgeProfile] = [
            KnowledgeProfile(topic=profile.topic, score=profile.get_percentage_score())
            for profile in student_summary.knowledge_profiles
        ]

        result = SummaryResponse(
            student_id=student_summary.student_id,
            name=student_summary.student_name,
            knowledge_classification=student_summary.knowledge_classification,
            profile=knowledge_profiles,
            feedback=student_summary.feedback,
        )
        return result
