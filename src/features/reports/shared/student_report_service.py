from pydantic import BaseModel
from itmentorsoft_persistence.repositories import (
    AssessmentRepository,
    ReportRepository,
)
from itmentorsoft_persistence.dto import (
    CategorySummary,
    PaginatedStudentSummary,
    StudentProgress,
    StudentSummary,
)
from itmentorsoft_persistence.repositories import UserRepository


class GetSummaryResponse(BaseModel):
    is_success: bool
    message: str
    student_summary: StudentSummary | None = None


class GetProgressByTopic(BaseModel):
    is_success: bool
    message: str
    historical_progress: StudentProgress | None = None


class GetCategorySummary(BaseModel):
    is_success: bool
    message: str
    category_summary: CategorySummary | None = None


class GetStudentsResponse(BaseModel):
    is_success: bool
    message: str
    students: PaginatedStudentSummary | None = None


class StudentReportService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        user_repository: UserRepository,
        report_repository: ReportRepository,
    ):
        self.assessment_repository = assessment_repository
        self.user_repository = user_repository
        self.report_repository = report_repository

    async def get_student_summary(self, user_id: str) -> GetSummaryResponse:
        """Obtain the student summary by user ID

        Args:
            user_id (str): The ID of the user to retrieve the student summary for.

        Returns:
            GetSummaryResponse: The student summary corresponding to the given user ID.
        """
        student_found = await self.user_repository.get_user_by_id(user_id)
        if not student_found:
            return GetSummaryResponse(
                is_success=False, message="Student not found", student_summary=None
            )

        response = await self.assessment_repository.get_student_summary(user_id)
        if not response or not response.knowledge_profiles:
            return GetSummaryResponse(
                is_success=False,
                message="Student summary not found",
                student_summary=None,
            )

        return GetSummaryResponse(
            is_success=True,
            message="Student summary retrieved successfully",
            student_summary=response,
        )

    async def get_student_progress(self, user_id: str) -> GetProgressByTopic:
        """Obtain the student progress by user ID

        Args:
            user_id (str): The ID of the user to retrieve the student progress for.

        Returns:
            GetProgressByTopic: The student progress corresponding to the given user ID.
        """
        student_found = await self.user_repository.get_user_by_id(user_id)
        if not student_found:
            return GetProgressByTopic(
                is_success=False, message="Student not found", historical_progress=None
            )

        response = await self.assessment_repository.get_student_progress(user_id)
        if not response or not response.historical_progress:
            return GetProgressByTopic(
                is_success=False,
                message="Student progress not found",
                historical_progress=None,
            )

        return GetProgressByTopic(
            is_success=True,
            message="Student progress retrieved successfully",
            historical_progress=response,
        )

    async def get_category_summary(self, category: str) -> GetCategorySummary:
        """Obtain the category summary by category name

        Args:
            category (str): The name of the category to retrieve the summary for.

        Returns:
            GetCategorySummary: The category summary corresponding to the given category name.
        """
        response = await self.report_repository.get_category_summary(category)
        if not response:
            return GetCategorySummary(
                is_success=False,
                message="Category summary not found",
                category_summary=None,
            )

        return GetCategorySummary(
            is_success=True,
            message="Category summary retrieved successfully",
            category_summary=response,
        )

    async def get_all_students(self, page: int, page_size: int) -> GetStudentsResponse:
        """Retrieve a list of all students.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of students per page.

        Returns:
            GetStudentsResponse: The response containing a paginated list of students.
        """
        response = await self.report_repository.get_all_students(page, page_size)
        if not response or not response.students:
            return GetStudentsResponse(
                is_success=False,
                message="Students not found",
                students=None,
            )

        return GetStudentsResponse(
            is_success=True,
            message="Students retrieved successfully",
            students=response,
        )

    async def get_all_students_by_category(
        self, category: str, page: int, page_size: int
    ) -> GetStudentsResponse:
        """Retrieve a list of all students filtered by category.

        Args:
            category (str): The category to filter students by.
            page (int): The page number to retrieve.
            page_size (int): The number of students per page.

        Returns:
            GetStudentsResponse: The response containing a paginated list of students filtered by category.
        """
        response = await self.report_repository.get_all_students_by_category(
            category, page, page_size
        )
        if not response or not response.students:
            return GetStudentsResponse(
                is_success=False,
                message="Students not found",
                students=None,
            )

        return GetStudentsResponse(
            is_success=True,
            message="Students retrieved successfully",
            students=response,
        )
