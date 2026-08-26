import os
from dotenv import load_dotenv
from datetime import datetime

from src.features.shared.notification_service import (
    NotificationConfigBuilder,
    NotificationService,
)
from src.features.shared.template_loader import TemplateLoader
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.features.user_management.shared.role_repository import RoleRepository
from src.features.user_management.shared.user_repository import UserRepository
from src.features.user_management.shared.user import (
    User,
    UserResponse,
    UserRole,
    UserStatus,
)

load_dotenv()


class CreateUserRequest:
    def __init__(self, email: str, username: str, password: str, role: str):
        self.email = email
        self.username = username
        self.password = password
        self.role = role


class CreateUserResponse:
    def __init__(self, is_success: bool, message: str, user_id: str = ""):
        self.is_success = is_success
        self.message = message
        self.user_id = user_id


class GetUsersByRoleResponse:
    def __init__(self, is_success: bool, message: str, users: list[UserResponse]):
        self.is_success = is_success
        self.message = message
        self.users = users


LOGIN_URL_BASE = os.getenv("LOGIN_URL_BASE", "")


class UserManagerService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        role_repository: RoleRepository,
        notification_service: NotificationService,
        template_loader: TemplateLoader,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.role_repository = role_repository
        self.notification_service = notification_service
        self.template_loader = template_loader

    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        """Create a new user based on the provided request data.

        Args:
            request (CreateUserRequest): Request object containing the user data for creation

        Returns:
            CreateUserResponse: Response object containing the result of the user creation process
        """
        if await self.user_repository.get_user_by_email(request.email):
            return CreateUserResponse(is_success=False, message="Email already in use")

        if await self.user_repository.get_user_by_username(request.username):
            return CreateUserResponse(
                is_success=False, message="Username already in use"
            )
        role = await self.role_repository.get_role_by_name(request.role)
        if not role:
            return CreateUserResponse(
                is_success=False, message="Invalid role specified"
            )
        user_role = UserRole(request.role)
        password_hashed = self.password_hasher.hash_password(request.password)
        user_entity = User(
            username=request.username,
            email=request.email,
            password_hashed=password_hashed,
            status=UserStatus.ACTIVE,
            role=user_role,
        )
        await self.user_repository.save(user_entity)

        notification_config_builder = NotificationConfigBuilder(
            request.email, "Your account has been created successfully"
        )

        try:
            html_content = self.template_loader.load("user_created")
            html_content = (
                html_content.replace("%USER%", request.username)
                .replace("%EMAIL%", request.email)
                .replace("%ROLE%", request.role)
                .replace(
                    "%REGISTER_DATE%", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                .replace("%LOGIN_URL%", LOGIN_URL_BASE)
            )
            notification_config_builder.set_template(html_content)
            notification_config = notification_config_builder.build()

            _ = await self.notification_service.send_notification(notification_config)
        except FileNotFoundError:
            print("Email template not found. Please contact support.")

        return CreateUserResponse(
            is_success=True, message="User created successfully", user_id=user_entity.id
        )

    async def get_users_by_role(self, role: str) -> GetUsersByRoleResponse:
        """Retrieve users by their role.

        Args:
            role (str): The role to filter users by.

        Returns:
            GetUsersByRoleResponse: Response object containing the result of the query.
        """

        role_entity = await self.role_repository.get_role_by_name(role)
        if not role_entity:
            return GetUsersByRoleResponse(
                is_success=False, message="Invalid role specified", users=[]
            )

        users = await self.user_repository.get_users_by_role(role)

        if not users:
            return GetUsersByRoleResponse(
                is_success=False,
                message="No users found for the specified role",
                users=[],
            )

        return GetUsersByRoleResponse(
            is_success=True, message="Users retrieved successfully", users=users
        )
