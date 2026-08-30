from src.features.user_management.shared.user import (
    CompleteUserResponse,
    User,
    UserRole,
    UserStatus,
    UserResponse,
)
from src.infrastructure.database.postgresql.models.postgresql_user_model import (
    UserEntity,
)


class PostgresUserMapper:

    @staticmethod
    def to_entity(user_model: User) -> UserEntity:
        """Map user domain model into user entity.

        Args:
            user_model (User): User domain model

        Returns:
            UserEntity: User entity
        """
        return UserEntity(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            name=user_model.name,
            hashed_password=user_model.password_hashed,
            status=user_model.status.value,
            role_id=user_model.role_id,
        )

    @staticmethod
    def to_model(user_entity: UserEntity) -> User:
        """Map user entity into user domain model.

        Args:
            user_entity (UserEntity): User entity
        Returns:
            User: User domain model
        """
        role_value: str = (
            user_entity.role.name
            if user_entity.role is not None
            else UserRole.USER.value
        )
        user = User(
            username=user_entity.username,
            email=user_entity.email,
            name=user_entity.name,
            password_hashed=user_entity.hashed_password,
            status=UserStatus(user_entity.status),
            role=UserRole(role_value),
        )
        if user_entity.role_id:
            user.set_role_id(user_entity.role_id)
        return user

    @staticmethod
    def to_response(user_entity: UserEntity) -> UserResponse:
        """Map user entity into user response.

        Args:
            user_entity (UserEntity): User entity
        Returns:
            UserResponse: User response
        """
        role_value: str = (
            user_entity.role.name
            if user_entity.role is not None
            else UserRole.USER.value
        )
        return UserResponse(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            name=user_entity.name,
            status=UserStatus(user_entity.status),
            role=UserRole(role_value),
        )

    @staticmethod
    def to_complete_response(user_entity: UserEntity) -> CompleteUserResponse:
        """Map user entity into complete user response.

        Args:
            user_entity (UserEntity): User entity
        Returns:
            CompleteUserResponse: Complete user response
        """
        role_value: str = (
            user_entity.role.name
            if user_entity.role is not None
            else UserRole.USER.value
        )
        return CompleteUserResponse(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            password_hashed=user_entity.hashed_password,
            status=UserStatus(user_entity.status),
            role=UserRole(role_value),
        )
