from typing import Type
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from itmentorsoft_persistence.dto import (
    ContentByTopic,
    LearningPath,
    LearningPathProgress,
    LearningPathProgressResponse,
    LearningPathResponse,
)
from itmentorsoft_persistence.repositories import (
    LearningPathRepository,
)
from itmentorsoft_persistence.models import (
    LearningPathEntity,
    TopicResultEntity,
    ContentRating,
    LearningPathContentEntity,
    ResourceContentEntity,
)
from itmentorsoft_persistence.mappers import (
    PostgresLearningPathMapper,
)
from sqlalchemy.orm import selectinload


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
                path_id="",
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
            path_id=uuid.uuid4().hex,
            recommendation=learning_paths,
        )

    async def save_learning_path(self, learning_path: LearningPath):
        learning_path_entity = self.mapper.to_learning_path_entity(learning_path)
        learning_path_contents = self.mapper.to_learning_path_contents(learning_path)

        self.session_factory.add(learning_path_entity)
        self.session_factory.add_all(learning_path_contents)
        await self.session_factory.commit()

    async def update_status_content_path(
        self, path_id: str, content_id: str, status: bool
    ) -> LearningPathProgressResponse:
        smt = select(LearningPathContentEntity).where(
            LearningPathContentEntity.learning_path_id == path_id,
            LearningPathContentEntity.content_id == content_id,
        )
        result_content_path = await self.session_factory.execute(smt)
        content_path = result_content_path.scalars().one()
        if not content_path:
            return LearningPathProgressResponse(
                is_success=False,
                message="Content path not found.",
                path_progress=None,
            )

        content_path.is_completed = status
        await self.session_factory.commit()

        progress = await self.get_learning_path_progress(path_id)
        if not progress.is_success:
            return LearningPathProgressResponse(
                is_success=False,
                message="Learning path not found.",
                path_progress=None,
            )

        return LearningPathProgressResponse(
            is_success=True,
            message="Content path status updated successfully.",
            path_progress=progress.path_progress,
        )

    async def get_learning_path_progress(
        self, path_id: str
    ) -> LearningPathProgressResponse:
        stmt = select(LearningPathContentEntity).where(
            LearningPathContentEntity.learning_path_id == path_id
        )
        result = await self.session_factory.execute(stmt)
        contents = result.scalars().all()
        if not contents:
            return LearningPathProgressResponse(
                is_success=False,
                message="Learning path not found.",
                path_progress=None,
            )
        total = len(contents)
        completed = sum(1 for content in contents if content.is_completed)
        progress = (completed / total) * 100 if total > 0 else 0.0
        return LearningPathProgressResponse(
            is_success=True,
            message="Learning path progress retrieved successfully.",
            path_progress=LearningPathProgress(path_id=path_id, progress=progress),
        )

    async def is_learning_path_created(self, user_id: str) -> bool:
        stmt = select(LearningPathEntity).where(
            LearningPathEntity.user_id == user_id,
        )
        result = await self.session_factory.execute(stmt)
        learning_path = result.scalars().first()
        return learning_path is not None and not learning_path.is_completed

    async def get_learning_path_by_id(self, path_id: str) -> LearningPath | None:
        stmt = (
            select(LearningPathEntity)
            .options(
                selectinload(LearningPathEntity.contents).options(
                    selectinload(LearningPathContentEntity.content)
                )
            )
            .where(LearningPathEntity.id == path_id)
        )
        result = await self.session_factory.execute(stmt)
        learning_path = result.scalars().first()
        if not learning_path:
            return None

        smt_ratings = select(ContentRating.content_id, ContentRating.rating).where(
            ContentRating.content_id.in_(
                [content.content.id for content in learning_path.contents]
            )
        )
        result_ratings = await self.session_factory.execute(smt_ratings)
        all_ratings = result_ratings.fetchall()
        content_ratings = {}
        for content_id, rating in all_ratings:
            if content_id not in content_ratings:
                content_ratings[content_id] = []
            content_ratings[content_id].append(rating)

        average_ratings = {
            content_id: sum(ratings) / len(ratings) if ratings else 0.0
            for content_id, ratings in content_ratings.items()
        }

        learning_path_progress = await self.get_learning_path_progress(learning_path.id)

        return LearningPath(
            path_id=learning_path.id,
            user_id=learning_path.user_id,
            is_completed=learning_path.is_completed,
            topic=learning_path.topic,
            progress=(
                learning_path_progress.path_progress.progress
                if learning_path_progress and learning_path_progress.path_progress
                else 0.0
            ),
            contents=[
                ContentByTopic(
                    content_id=content.content.id,
                    title=content.content.title,
                    description=content.content.summary,
                    rating=average_ratings.get(content.content.id, 0.0),
                )
                for content in learning_path.contents
            ],
        )

    async def is_path_associated_with_user(self, path_id: str, user_id: str) -> bool:
        stmt = select(LearningPathEntity).where(
            LearningPathEntity.user_id == user_id, LearningPathEntity.id == path_id
        )
        result = await self.session_factory.execute(stmt)
        learning_path = result.scalars().first()
        return learning_path is not None
