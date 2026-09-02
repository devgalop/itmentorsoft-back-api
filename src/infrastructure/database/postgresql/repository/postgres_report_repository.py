from typing import Type

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from itmentorsoft_persistence.dto import (
    CategorySummary,
    PaginatedStudentSummary,
    StudentBasicSummary,
)
from itmentorsoft_persistence.repositories import ReportRepository
from itmentorsoft_persistence.models import (
    ClassificationResultEntity,
)
from itmentorsoft_persistence.mappers import (
    PostgresReportMapper,
)


class PostgresReportRepository(ReportRepository):
    def __init__(
        self, session_factory: AsyncSession, mapper: Type[PostgresReportMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def get_all_students(
        self, page: int, page_size: int
    ) -> PaginatedStudentSummary:
        count_smt = (
            select(func.count(func.distinct(ClassificationResultEntity.user_id)))
            .select_from(ClassificationResultEntity)
            .where(ClassificationResultEntity.is_enabled)
        )
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedStudentSummary(students=[], total_students=0, page=page)

        smt = (
            select(ClassificationResultEntity)
            .options(selectinload(ClassificationResultEntity.user))
            .where(ClassificationResultEntity.is_enabled)
            .offset(page * page_size)
            .limit(page_size)
        )
        result = await self.session_factory.execute(smt)
        classification_result_entities = result.scalars().all()
        students_summary: list[StudentBasicSummary] = []
        for entity in classification_result_entities:
            students_summary.append(
                self.mapper.from_classification_result_to_student_basic_summary(entity)
            )

        return PaginatedStudentSummary(
            students=students_summary, total_students=total, page=page
        )

    async def get_all_students_by_category(
        self, category: str, page: int, page_size: int
    ) -> PaginatedStudentSummary:
        count_smt = (
            select(func.count(func.distinct(ClassificationResultEntity.user_id)))
            .select_from(ClassificationResultEntity)
            .where(
                ClassificationResultEntity.classification == category,
                ClassificationResultEntity.is_enabled,
            )
        )
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedStudentSummary(students=[], total_students=0, page=page)

        smt = (
            select(ClassificationResultEntity)
            .options(selectinload(ClassificationResultEntity.user))
            .where(
                ClassificationResultEntity.classification == category,
                ClassificationResultEntity.is_enabled,
            )
            .offset(page * page_size)
            .limit(page_size)
        )
        result = await self.session_factory.execute(smt)
        classification_result_entities = result.scalars().all()
        students_summary: list[StudentBasicSummary] = []
        for entity in classification_result_entities:
            students_summary.append(
                self.mapper.from_classification_result_to_student_basic_summary(entity)
            )

        return PaginatedStudentSummary(
            students=students_summary, total_students=total, page=page
        )

    async def get_category_summary(self, category: str) -> CategorySummary:
        count_smt = (
            select(func.count(func.distinct(ClassificationResultEntity.user_id)))
            .select_from(ClassificationResultEntity)
            .where(
                ClassificationResultEntity.classification == category,
                ClassificationResultEntity.is_enabled,
            )
        )
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return CategorySummary(category=category, total_students=0)
        return CategorySummary(category=category, total_students=total)
