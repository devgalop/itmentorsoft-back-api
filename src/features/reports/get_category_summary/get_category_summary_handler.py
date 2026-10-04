from src.i18n import t
from src.features.reports.get_category_summary.get_category_summary_request import (
    GetCategorySummaryRequest,
)
from src.features.reports.get_category_summary.get_category_summary_response import (
    CategorySummary,
    GetCategorySummaryResponse,
)
from src.features.reports.shared.student_report_service import (
    GetCategorySummary,
    StudentReportService,
)


class GetCategorySummaryHandler:
    def __init__(self, report_service: StudentReportService):
        self.report_service = report_service

    async def handle(
        self, request: GetCategorySummaryRequest
    ) -> GetCategorySummaryResponse:
        """Handle the request to get category summary.

        Args:
            request (GetCategorySummaryRequest): The request containing the category.

        Returns:
            GetCategorySummaryResponse: The response containing the category summary.
        """
        response = await self.report_service.get_category_summary(request.category)
        summary = self.map_to_response(response)
        if summary.category == "" and summary.total_students == 0:
            return GetCategorySummaryResponse(
                is_success=False,
                message=t("report.category_summary.not_found"),
                category_summary=summary,
            )
        return GetCategorySummaryResponse(
            is_success=response.is_success,
            message=response.message,
            category_summary=summary,
        )

    def map_to_response(self, summary: GetCategorySummary) -> CategorySummary:
        """Map the GetCategorySummary object to CategorySummary.

        Args:
            summary (GetCategorySummary): The GetCategorySummary object.

        Returns:
            CategorySummary: The mapped CategorySummary object.
        """
        if not summary or not summary.category_summary:
            return CategorySummary(category="", total_students=0)
        return CategorySummary(
            category=summary.category_summary.category,
            total_students=summary.category_summary.total_students,
        )
