from src.features.reports.get_student_progress.get_student_progress_request import (
    GetStudentProgressRequest,
)
from src.features.reports.get_student_progress.get_student_progress_response import (
    GetStudentProgressResponse,
    KnowledgeProfile,
    ProgressResponse,
)
from itmentorsoft_persistence.dto import StudentProgress
from src.features.reports.shared.student_report_service import StudentReportService


class GetStudentProgressHandler:
    def __init__(self, student_report_service: StudentReportService):
        self.student_report_service = student_report_service

    async def handle(
        self, request: GetStudentProgressRequest
    ) -> GetStudentProgressResponse:
        """Handle the request to get student progress by user ID.

        Args:
            request (GetStudentProgressRequest): The request containing the user ID.

        Returns:
            GetStudentProgressResponse: The response containing the student progress.
        """
        response = await self.student_report_service.get_student_progress(
            request.student_id
        )

        if not response.is_success or not response.historical_progress:
            return GetStudentProgressResponse(
                is_success=False, message=response.message, progress=None
            )

        result = self.map_to_response(response.historical_progress)
        return GetStudentProgressResponse(
            is_success=True, message=response.message, progress=result
        )

    def map_to_response(self, student_progress: StudentProgress) -> ProgressResponse:
        """Map the student progress to the response model.

        Args:
            student_progress (StudentProgress): The student progress to be mapped.

        Returns:
            ProgressResponse: The mapped response model.
        """
        results: list[KnowledgeProfile] = []
        for progress_by_topic in student_progress.historical_progress:
            for result in progress_by_topic.result:
                results.append(
                    KnowledgeProfile(
                        topic=progress_by_topic.topic,
                        score=result.get_percentage_score(),
                        index=result.index,
                    )
                )

        return ProgressResponse(
            student_id=student_progress.student_id,
            classification=student_progress.classification,
            knowledge_profile=results,
            feedback=student_progress.feedback,
        )
