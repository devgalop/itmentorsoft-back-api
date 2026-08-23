from typing import Type
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.content_management.shared.learning_path import (
    ContentByTopic,
    LearningPath,
    LearningPathResponse,
)
from src.features.content_management.shared.learning_path_repository import (
    LearningPathRepository,
)
from src.infrastructure.database.postgresql.models.postgresql_assessment_model import (
    TopicResultEntity,
)
from src.infrastructure.database.postgresql.models.postgresql_content_rating import (
    ContentRating,
)
from src.infrastructure.database.postgresql.models.postgresql_learning_path_mapper import (
    PostgresLearningPathMapper,
)
from src.infrastructure.database.postgresql.models.postgresql_resource_content import (
    ResourceContentEntity,
)


class PostgresLearningPathRepository(LearningPathRepository):
    def __init__(
        self, session_factory: AsyncSession, mapper: Type[PostgresLearningPathMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def get_learning_path(self, user_id: str) -> LearningPathResponse:
        # 1. Buscar por estudiante el puntaje por tema
        smt = select(TopicResultEntity).where(
            TopicResultEntity.user_id == user_id, TopicResultEntity.is_enabled
        )
        results = await self.session_factory.execute(smt)
        results = results.scalars().all()
        if not results:
            return LearningPathResponse(
                is_success=False,
                message="No se encontraron resultados de evaluación para el usuario.",
                recommendation=[],
            )
        # 2. Para cada tema, buscar el top 5 de contenidos con mejor puntaje
        learning_paths = []
        for result in results:
            topic = result.topic
            stmt = (
                select(
                    ResourceContentEntity,
                    func.avg(ContentRating.rating).label("avg_rating"),
                )
                .join(
                    ContentRating, ResourceContentEntity.id == ContentRating.content_id
                )
                .where(ResourceContentEntity.related_topics.ilike(f"%{topic}%"))
                .group_by(ResourceContentEntity.id)
                .order_by(func.avg(ContentRating.rating).desc())
                .limit(5)
            )
            content_results = await self.session_factory.execute(stmt)
            if not content_results:
                continue
            contents = [
                ContentByTopic(
                    content_id=content.id,
                    title=content.title,
                    description=content.summary,
                    rating=float(avg_rating),
                )
                for content, avg_rating in content_results.all()
            ]
            # 3. Construir el LearningPath con los contenidos obtenidos
            learning_path = LearningPath(
                path_id=uuid.uuid4().hex,
                user_id=user_id,
                topic=topic,
                is_completed=False,
                contents=contents,
            )
            learning_paths.append(learning_path)

        return LearningPathResponse(
            is_success=True,
            message="Learning paths retrieved successfully.",
            recommendation=learning_paths,
        )

    async def save_learning_path(self, learning_path: LearningPath):
        learning_path_entity = self.mapper.to_learning_path_entity(learning_path)
        learning_path_contents = self.mapper.to_learning_path_contents(learning_path)

        self.session_factory.add(learning_path_entity)
        self.session_factory.add_all(learning_path_contents)
        await self.session_factory.commit()
