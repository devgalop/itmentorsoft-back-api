from src.features.user_management.create_user.create_user_request import (
    CreateUserRequest,
)
from src.features.user_management.create_user.create_user_response import (
    CreateUserResponse,
)
from src.features.user_management.shared.password_hasher import PasswordHasher
from itmentorsoft_persistence.repositories import (
    RoleRepository,
    UserRepository,
)
from itmentorsoft_persistence.dto import (
    User,
    UserRole,
    UserStatus,
)


class CreateUserHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        role_repository: RoleRepository,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.role_repository = role_repository

    async def handle(self, user_data: CreateUserRequest) -> CreateUserResponse:
        if await self.user_repository.get_user_by_email(user_data.email):
            return CreateUserResponse(is_success=False, message="Email already in use")

        if await self.user_repository.get_user_by_username(user_data.username):
            return CreateUserResponse(
                is_success=False, message="Username already in use"
            )
        default_role = await self.role_repository.get_role_by_name(
            UserRole.STUDENT.value
        )
        password_hashed = self.password_hasher.hash_password(user_data.password)
        user_entity = User(
            username=user_data.username,
            email=user_data.email,
            name=user_data.name,
            password_hashed=password_hashed,
            status=UserStatus.ACTIVE,
            role=UserRole.STUDENT,
        )
        if default_role:
            user_entity.set_role_id(default_role.role_id)
        await self.user_repository.save(user_entity)

        return CreateUserResponse(
            is_success=True, message="User created successfully", user_id=user_entity.id
        )
