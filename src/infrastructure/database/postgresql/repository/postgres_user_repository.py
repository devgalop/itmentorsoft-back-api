from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from itmentorsoft_persistence.dto import (
    AssignRoleToUserCommand,
    CompleteUserResponse,
    User,
    UserResponse,
    UserRole,
    UserStatus,
)
from itmentorsoft_persistence.repositories import UserRepository
from itmentorsoft_persistence.models import (
    RoleEntity,
    UserEntity,
)
from itmentorsoft_persistence.mappers import (
    PostgresUserMapper,
)


class PostgresUserRepository(UserRepository):

    def __init__(
        self, session_factory: AsyncSession, user_mapper: Type[PostgresUserMapper]
    ):
        self.session_factory = session_factory
        self.user_mapper = user_mapper

    async def get_user_by_username(self, username: str) -> CompleteUserResponse | None:
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(UserEntity.username == username)
        )
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_complete_response(user_found)

    async def get_user_by_email(self, email: str) -> CompleteUserResponse | None:
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(UserEntity.email == email)
        )
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_complete_response(user_found)

    async def get_user_response_by_email(self, email: str) -> UserResponse | None:
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(UserEntity.email == email)
        )
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_response(user_found)

    async def get_user_by_id(self, user_id: str) -> UserResponse | None:
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(UserEntity.id == user_id)
        )
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        return self.user_mapper.to_response(user_found)

    async def save(self, user: User):
        user_entity = self.user_mapper.to_entity(user)
        self.session_factory.add(user_entity)
        await self.session_factory.commit()

    async def change_password(self, user_id: str, new_password_hashed: str):
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(UserEntity.id == user_id)
        )
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        user_found.hashed_password = new_password_hashed
        await self.session_factory.commit()

    async def assign_role_to_user(self, request: AssignRoleToUserCommand):
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(UserEntity.id == request.user_id)
        )
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        user_found.role_id = request.role_id
        await self.session_factory.commit()

    async def get_available_roles(self) -> list[str]:
        return [role.value for role in UserRole]

    async def get_admin_users(self) -> list[UserResponse]:
        role_stmt = select(RoleEntity).where(RoleEntity.name == UserRole.ADMIN.value)
        role = await self.session_factory.execute(role_stmt)
        role = role.scalars().first()
        if not role:
            return []
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(UserEntity.role_id == role.id)
        )
        result = await self.session_factory.execute(stmt)
        users_found = result.scalars().all()
        if not users_found:
            return []
        return [self.user_mapper.to_response(user) for user in users_found]

    async def get_users_by_role(self, role: str) -> list[UserResponse]:
        role_stmt = select(RoleEntity).where(RoleEntity.name == role)
        role_result = await self.session_factory.execute(role_stmt)
        role_entity = role_result.scalars().first()
        if not role_entity:
            return []
        stmt = (
            select(UserEntity)
            .options(selectinload(UserEntity.role))
            .where(
                UserEntity.role_id == role_entity.id,
                UserEntity.status == UserStatus.ACTIVE.value,
            )
        )
        result = await self.session_factory.execute(stmt)
        users_found = result.scalars().all()
        if not users_found:
            return []
        return [self.user_mapper.to_response(user) for user in users_found]

    async def update_user_status(self, user_id: str, new_status: str):
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        user_found.status = new_status
        await self.session_factory.commit()

    async def update_username(self, user_id: str, new_username: str, name: str):
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.session_factory.execute(stmt)
        user_found = result.scalars().first()
        if not user_found:
            return None
        user_found.username = new_username
        user_found.name = name
        await self.session_factory.commit()
