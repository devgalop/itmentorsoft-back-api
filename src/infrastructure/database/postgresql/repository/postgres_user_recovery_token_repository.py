from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from itmentorsoft_persistence.dto import (
    RecoveryTokenInfo,
    UserRecoveryTokenResponse,
)
from itmentorsoft_persistence.repositories import (
    UserRecoveryTokenRepository,
)
from itmentorsoft_persistence.mappers import (
    PostgresRecoveryTokenMapper,
)
from itmentorsoft_persistence.models import (
    RecoveryTokenEntity,
)


class PostgresUserRecoveryTokenRepository(UserRecoveryTokenRepository):

    def __init__(
        self, session_factory: AsyncSession, mapper: Type[PostgresRecoveryTokenMapper]
    ):
        self.session_factory = session_factory
        self.mapper = mapper

    async def save_token(self, recovery_token_info: RecoveryTokenInfo):
        entity = self.mapper.to_entity(recovery_token_info)
        self.session_factory.add(entity)
        await self.session_factory.commit()

    async def get_user_id_by_transaction_id(
        self, transaction_id: str
    ) -> UserRecoveryTokenResponse | None:
        stmt = select(RecoveryTokenEntity).where(
            RecoveryTokenEntity.id == transaction_id
        )
        result = await self.session_factory.execute(stmt)
        token_found = result.scalars().first()
        if not token_found or token_found.status != "active":
            return None
        return self.mapper.to_model(token_found)

    async def revoke_tokens_by_user_id(self, user_id: str):
        stmt = select(RecoveryTokenEntity).where(RecoveryTokenEntity.user_id == user_id)
        result = await self.session_factory.execute(stmt)
        tokens_to_revoke = result.scalars().all()
        for token in tokens_to_revoke:
            token.status = "revoked"
        await self.session_factory.commit()
