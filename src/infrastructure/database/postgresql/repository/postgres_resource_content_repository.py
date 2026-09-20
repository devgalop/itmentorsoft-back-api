from typing import Type
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from itmentorsoft_persistence.dto import (
    GetContentsByCategoryPaginationRequest,
    GetContentsByCategoryTopicPaginationRequest,
    GetContentsByTitlePaginationRequest,
    GetContentsByTopicPaginationRequest,
    RateContent,
    PaginatedResourceContentResult,
    ResourceContent,
    ResourceContentRating,
    ResourceContentResponse,
    UpdateResourceContentRequest,
    ResourceContentRatingByStudent,
)

from itmentorsoft_persistence.repositories import (
    ResourceContentRepository,
)
from itmentorsoft_persistence.models import (
    ContentRating,
    ResourceContentEntity,
)
from itmentorsoft_persistence.mappers import (
    RateContentMapper,
    ResourceContentMapper,
)
from sqlalchemy.orm import selectinload


class PostgresResourceContentRepository(ResourceContentRepository):

    def __init__(
        self,
        session_factory: AsyncSession,
        mapper: Type[ResourceContentMapper],
        rating_mapper: Type[RateContentMapper],
    ):
        self.session_factory = session_factory
        self.mapper = mapper
        self.rating_mapper = rating_mapper

    async def save(self, content: ResourceContent):
        entity = self.mapper.to_entity(content)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_resource_content(
        self, content_id: str
    ) -> ResourceContentResponse | None:
        smt = select(ResourceContentEntity).where(
            ResourceContentEntity.id == content_id
        )
        result = await self.session_factory.execute(smt)
        content_entity = result.scalars().first()
        if not content_entity:
            return None
        return self.mapper.to_model(content_entity)

    async def get_resource_contents_by_category(
        self, request: GetContentsByCategoryPaginationRequest
    ) -> PaginatedResourceContentResult:
        count_smt = (
            select(func.count())
            .select_from(ResourceContentEntity)
            .where(ResourceContentEntity.category == request.category)
            .where(ResourceContentEntity.is_enabled)
        )
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedResourceContentResult(items=[], total=0)
        smt = (
            select(ResourceContentEntity)
            .where(ResourceContentEntity.category == request.category)
            .where(ResourceContentEntity.is_enabled)
            .offset(request.page * request.page_size)
            .limit(request.page_size)
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return PaginatedResourceContentResult(
            items=[self.mapper.to_model(entity) for entity in content_entities],
            total=total,
        )

    async def get_resource_contents_by_related_topic(
        self, request: GetContentsByTopicPaginationRequest
    ) -> PaginatedResourceContentResult:
        count_smt = (
            select(func.count())
            .select_from(ResourceContentEntity)
            .where(ResourceContentEntity.related_topics.ilike(f"%{request.topic}%"))
            .where(ResourceContentEntity.is_enabled)
        )
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedResourceContentResult(items=[], total=0)

        smt = (
            select(ResourceContentEntity)
            .where(ResourceContentEntity.related_topics.ilike(f"%{request.topic}%"))
            .where(ResourceContentEntity.is_enabled)
            .offset(request.page * request.page_size)
            .limit(request.page_size)
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return PaginatedResourceContentResult(
            items=[self.mapper.to_model(entity) for entity in content_entities],
            total=total,
        )

    async def get_resource_contents_by_title(
        self, request: GetContentsByTitlePaginationRequest
    ) -> PaginatedResourceContentResult:
        count_smt = (
            select(func.count())
            .select_from(ResourceContentEntity)
            .where(ResourceContentEntity.title.ilike(f"%{request.title}%"))
            .where(ResourceContentEntity.is_enabled)
        )
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedResourceContentResult(items=[], total=0)
        smt = (
            select(ResourceContentEntity)
            .where(ResourceContentEntity.title.ilike(f"%{request.title}%"))
            .where(ResourceContentEntity.is_enabled)
            .offset(request.page * request.page_size)
            .limit(request.page_size)
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return PaginatedResourceContentResult(
            items=[self.mapper.to_model(entity) for entity in content_entities],
            total=total,
        )

    async def get_resource_contents_by_category_and_related_topic(
        self, request: GetContentsByCategoryTopicPaginationRequest
    ) -> PaginatedResourceContentResult:
        count_smt = (
            select(func.count())
            .select_from(ResourceContentEntity)
            .where(ResourceContentEntity.category == request.category)
            .where(ResourceContentEntity.related_topics.ilike(f"%{request.topic}%"))
            .where(ResourceContentEntity.is_enabled)
        )
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedResourceContentResult(items=[], total=0)
        smt = (
            select(ResourceContentEntity)
            .where(ResourceContentEntity.category == request.category)
            .where(ResourceContentEntity.related_topics.ilike(f"%{request.topic}%"))
            .where(ResourceContentEntity.is_enabled)
            .offset(request.page * request.page_size)
            .limit(request.page_size)
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.scalars().all()
        return PaginatedResourceContentResult(
            items=[self.mapper.to_model(entity) for entity in content_entities],
            total=total,
        )

    async def rate_resource_content(self, request: RateContent):
        entity = self.rating_mapper.to_entity(request)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_all_resource_contents(
        self, page: int, page_size: int
    ) -> PaginatedResourceContentResult:
        count_smt = select(func.count()).select_from(ResourceContentEntity)
        total_result = await self.session_factory.execute(count_smt)
        total = total_result.scalar()
        if not total:
            return PaginatedResourceContentResult(items=[], total=0)
        smt = select(ResourceContentEntity).offset(page * page_size).limit(page_size)
        result = await self.session_factory.execute(smt)
        result_items = result.scalars().all()
        items = [self.mapper.to_model(item) for item in result_items]

        return PaginatedResourceContentResult(items=items, total=total)

    async def update_resource_content(
        self, content_id: str, request: UpdateResourceContentRequest
    ):
        smt = select(ResourceContentEntity).where(
            ResourceContentEntity.id == content_id
        )
        result = await self.session_factory.execute(smt)
        content_entity = result.scalars().first()

        if not content_entity:
            raise ValueError(f"Content with ID {content_id} not found.")

        content_entity.title = request.title
        content_entity.summary = request.description
        content_entity.url = request.url
        content_entity.category = request.category
        content_entity.related_topics = "|".join(request.related_topic)

        self.session_factory.add(content_entity)
        await self.session_factory.commit()

    async def update_resource_status(self, content_id: str, new_status: bool) -> bool:
        smt = select(ResourceContentEntity).where(
            ResourceContentEntity.id == content_id
        )
        result = await self.session_factory.execute(smt)
        content_entity = result.scalars().first()

        if not content_entity:
            return False

        content_entity.is_enabled = new_status
        self.session_factory.add(content_entity)
        await self.session_factory.commit()
        return True

    async def get_top_content(
        self, topic: str, limit: int, order: str = "desc"
    ) -> list[ResourceContentRating]:
        smt = (
            select(
                ResourceContentEntity,
                func.avg(ContentRating.rating).label("avg_rating"),
            )
            .join(ContentRating, ResourceContentEntity.id == ContentRating.content_id)
            .where(ResourceContentEntity.related_topics.ilike(f"%{topic}%"))
            .group_by(ResourceContentEntity.id)
            .order_by(
                func.avg(ContentRating.rating).desc()
                if order == "desc"
                else func.avg(ContentRating.rating).asc()
            )
            .limit(limit)
        )
        result = await self.session_factory.execute(smt)
        content_entities = result.all()
        if not content_entities:
            return []
        return [
            ResourceContentRating(
                content_id=entity.id,
                title=entity.title,
                summary=entity.summary,
                rating=avg_rating,
            )
            for entity, avg_rating in content_entities
        ]

    async def get_ratings_by_user(
        self, user_id: str
    ) -> list[ResourceContentRatingByStudent]:
        smt = (
            select(ContentRating)
            .options(selectinload(ContentRating.content))
            .where(ContentRating.user_id == user_id)
        )
        result = await self.session_factory.execute(smt)
        ratings = result.scalars().all()
        if not ratings:
            return []
        return [
            ResourceContentRatingByStudent(
                content_id=rating.content_id,
                title=rating.content.title,
                summary=rating.content.summary,
                rating=rating.rating,
                student_id=rating.user_id,
            )
            for rating in ratings
        ]

    async def get_rating_content_by_user(
        self, user_id: str, content_id: str
    ) -> ResourceContentRatingByStudent | None:
        smt = (
            select(ContentRating)
            .options(selectinload(ContentRating.content))
            .where(
                ContentRating.user_id == user_id, ContentRating.content_id == content_id
            )
        )
        result = await self.session_factory.execute(smt)
        rating = result.scalars().first()
        if not rating:
            return None
        return ResourceContentRatingByStudent(
            content_id=rating.content_id,
            title=rating.content.title,
            summary=rating.content.summary,
            rating=rating.rating,
            student_id=rating.user_id,
        )

    async def update_rating(self, request: RateContent):
        smt = select(ContentRating).where(
            ContentRating.user_id == request.user_id,
            ContentRating.content_id == request.content_id,
        )
        result = await self.session_factory.execute(smt)
        rating = result.scalars().first()
        if not rating:
            return
        rating.rating = request.rating
        rating.comment = request.comment
        await self.session_factory.commit()
