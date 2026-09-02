from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from itmentorsoft_persistence.dto import (
    EvaluativeQuestion,
    QuestionDifficulty,
)
from itmentorsoft_persistence.repositories import (
    QuestionAssessmentRepository,
)
from itmentorsoft_persistence.mappers import (
    PostgresQuestionMapper,
)
from itmentorsoft_persistence.models import (
    QuestionEntity,
)


class PostgresQuestionsAssessmentRepository(QuestionAssessmentRepository):
    def __init__(
        self, session_factory: AsyncSession, mapper: Type[PostgresQuestionMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def get_question_by_level(
        self, difficulty: QuestionDifficulty
    ) -> list[EvaluativeQuestion]:
        smt = select(QuestionEntity).where(
            QuestionEntity.difficulty == difficulty.value
        )
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        return [self.mapper.to_evaluative_model(entity) for entity in question_entities]

    async def get_questions_by_category(
        self, category: str
    ) -> list[EvaluativeQuestion]:
        smt = select(QuestionEntity).where(QuestionEntity.classification == category)
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        return [self.mapper.to_evaluative_model(entity) for entity in question_entities]

    async def get_questions_by_topic(
        self, topic: str, difficulty: QuestionDifficulty
    ) -> list[EvaluativeQuestion]:
        smt = select(QuestionEntity).where(
            QuestionEntity.classification == topic,
            QuestionEntity.difficulty == difficulty.value,
        )
        result = await self.session_factory.execute(smt)
        question_entities = result.scalars().all()
        return [self.mapper.to_evaluative_model(entity) for entity in question_entities]
