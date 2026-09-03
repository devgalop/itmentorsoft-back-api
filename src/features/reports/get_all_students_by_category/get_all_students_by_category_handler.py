from src.features.reports.get_all_students_by_category.get_all_students_by_category_request import (
    GetStudentsByCategoryRequest,
)
from src.features.reports.get_all_students_by_category.get_all_students_by_category_response import (
    GetStudentsByCategoryResponse,
    PaginatedStudentResult,
    StudentClassification,
)
from itmentorsoft_persistence.repositories import ReportRepository
from itmentorsoft_persistence.dto import PaginatedStudentSummary


class GetStudentsByCategoryHandler:
    def __init__(self, report_repository: ReportRepository):
        self.report_repository = report_repository

    async def handle(
        self, request: GetStudentsByCategoryRequest
    ) -> GetStudentsByCategoryResponse:
        paginated_result = await self.report_repository.get_all_students_by_category(
            category=request.category, page=request.page, page_size=request.page_size
        )
        return GetStudentsByCategoryResponse(
            is_success=True,
            message="Students retrieved successfully",
            result=self.map_to_response(paginated_result),
        )

    def map_to_response(
        self, result: PaginatedStudentSummary
    ) -> PaginatedStudentResult:
        if not result.students:
            return PaginatedStudentResult(
                students=[], total_students=0, page=result.page
            )
        return PaginatedStudentResult(
            students=[
                StudentClassification(
                    student_id=student.student_id,
                    student_name=student.student_name,
                    knowledge_classification=student.knowledge_classification,
                )
                for student in result.students
            ],
            total_students=result.total_students,
            page=result.page,
        )
