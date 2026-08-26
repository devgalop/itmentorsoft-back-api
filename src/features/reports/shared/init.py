from fastapi import APIRouter

from src.features.reports.get_student_summary.get_student_summary_endpoint import (
    router as get_student_summary_router,
)
from src.features.reports.get_all_students.get_all_students_endpoint import (
    router as get_all_students_router,
)
from src.features.reports.get_student_progress.get_student_progress_endpoint import (
    router as get_student_progress_router,
)
from src.features.reports.get_category_summary.get_category_summary_endpoint import (
    router as get_category_summary_router,
)
from src.features.reports.get_all_students_by_category.get_all_students_by_category_endpoint import (
    router as get_students_by_category_router,
)
from src.features.reports.get_users_by_role.get_users_by_role_endpoint import (
    router as get_users_by_role_router,
)

router = APIRouter()
router.include_router(get_student_summary_router)
router.include_router(get_student_progress_router)
router.include_router(get_category_summary_router)
router.include_router(get_all_students_router)
router.include_router(get_students_by_category_router)
router.include_router(get_users_by_role_router)
