from datetime import datetime, timezone
from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from itmentorsoft_persistence.repositories import (
    RefreshTokenRepository,
    RefreshTokenData,
    RefreshTokenInfo,
    TotalActiveUsers,
)
from itmentorsoft_persistence.mappers import (
    PostgresRefreshTokenMapper,
)
from itmentorsoft_persistence.models import (
    RefreshTokenEntity,
)


class PostgresUserRefreshTokenRepository(RefreshTokenRepository):

    def __init__(
        self, session_factory: AsyncSession, mapper: Type[PostgresRefreshTokenMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def save_token(self, info: RefreshTokenInfo):
        entity = self.mapper.to_entity(info)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_active_token(self, user_id: str) -> RefreshTokenData | None:
        stmt = select(RefreshTokenEntity).where(
            RefreshTokenEntity.status == "active", RefreshTokenEntity.user_id == user_id
        )
        result = await self.session_factory.execute(stmt)
        active_token = result.scalars().first()

        if not active_token:
            return None

        return self.mapper.to_model(active_token)

    async def revoke_tokens_by_user_id(self, user_id: str):
        stmt = select(RefreshTokenEntity).where(RefreshTokenEntity.user_id == user_id)
        result = await self.session_factory.execute(stmt)
        tokens_to_revoke = result.scalars().all()
        for token in tokens_to_revoke:
            token.status = "revoked"
        await self.session_factory.commit()

    async def get_users_with_active_tokens(self) -> TotalActiveUsers:
        timestamp_now = datetime.now(tz=timezone.utc).timestamp()
        stmt = select(RefreshTokenEntity.user_id).where(
            RefreshTokenEntity.status == "active",
            RefreshTokenEntity.expiration_time > timestamp_now,
        )
        result = await self.session_factory.execute(stmt)
        active_tokens = result.scalars().all()
        total_active_users = len(set(active_tokens))
        return TotalActiveUsers(total_active_users)
