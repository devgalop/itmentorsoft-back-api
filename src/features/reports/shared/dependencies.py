from fastapi.params import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from itmentorsoft_persistence.repositories import AssessmentRepository
from src.features.assessments.shared.dependencies import get_assessment_repository
from src.features.reports.get_all_students.get_all_students_handler import (
    GetAllStudentsHandler,
)
from src.features.reports.get_all_students_by_category.get_all_students_by_category_handler import (
    GetStudentsByCategoryHandler,
)
from src.features.reports.get_category_summary.get_category_summary_handler import (
    GetCategorySummaryHandler,
)
from src.features.reports.get_student_progress.get_student_progress_handler import (
    GetStudentProgressHandler,
)
from src.features.reports.get_student_summary.get_student_summary_handler import (
    GetStudentSummaryHandler,
)
from src.features.reports.get_users_by_role.get_users_by_role_handler import (
    GetUsersByRoleHandler,
)
from src.features.reports.shared.report_repository import ReportRepository
from src.features.reports.shared.student_report_service import StudentReportService
from src.features.user_management.shared.dependencies import (
    get_user_manager_service,
    get_user_repository,
)
from src.features.user_management.shared.user_manager_service import UserManagerService
from src.features.user_management.shared.user_repository import UserRepository
from itmentorsoft_persistence.mappers import PostgresReportMapper
from src.infrastructure.database.postgresql.repository.postgres_report_repository import (
    PostgresReportRepository,
)
from itmentorsoft_persistence import get_db


def get_report_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ReportRepository:
    return PostgresReportRepository(
        session_factory=session, mapper=PostgresReportMapper
    )


def get_student_report_service(
    assessment_repository: Annotated[
        AssessmentRepository, Depends(get_assessment_repository)
    ],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    report_repository: Annotated[ReportRepository, Depends(get_report_repository)],
) -> StudentReportService:
    return StudentReportService(
        assessment_repository=assessment_repository,
        user_repository=user_repository,
        report_repository=report_repository,
    )


def get_get_student_summary_handler(
    student_report_service: Annotated[
        StudentReportService, Depends(get_student_report_service)
    ],
) -> GetStudentSummaryHandler:
    return GetStudentSummaryHandler(student_report_service=student_report_service)


def get_get_student_progress_handler(
    student_report_service: Annotated[
        StudentReportService, Depends(get_student_report_service)
    ],
) -> GetStudentProgressHandler:
    return GetStudentProgressHandler(student_report_service=student_report_service)


def get_get_category_summary_handler(
    student_report_service: Annotated[
        StudentReportService, Depends(get_student_report_service)
    ],
) -> GetCategorySummaryHandler:
    return GetCategorySummaryHandler(report_service=student_report_service)


def get_get_all_students_handler(
    student_report_service: Annotated[
        StudentReportService, Depends(get_student_report_service)
    ],
) -> GetAllStudentsHandler:
    return GetAllStudentsHandler(report_service=student_report_service)


def get_get_students_by_category_handler(
    student_report_service: Annotated[
        StudentReportService, Depends(get_student_report_service)
    ],
) -> GetStudentsByCategoryHandler:
    return GetStudentsByCategoryHandler(
        report_repository=student_report_service.report_repository
    )


def get_get_users_by_role_handler(
    user_manager_service: Annotated[
        UserManagerService, Depends(get_user_manager_service)
    ],
) -> GetUsersByRoleHandler:
    return GetUsersByRoleHandler(user_manager_service=user_manager_service)
