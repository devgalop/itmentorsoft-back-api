from datetime import datetime
from time import time

from src.features.shared.notification_service import (
    NotificationConfigBuilder,
    NotificationService,
)
from src.features.shared.template_loader import TemplateLoader
from src.features.user_management.shared.otp_generator import OTPGenerator
from src.features.user_management.shared.password_hasher import PasswordHasher
from itmentorsoft_persistence.repositories import RoleRepository
from itmentorsoft_persistence.repositories import UserRepository
from itmentorsoft_persistence.dto import (
    IncrementLoginTryCounterRequest,
    User,
    UserAccessTries,
    UserOTPRequest,
    UserResponse,
    UserRole,
    UserStatus,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


class CreateUserRequest:
    def __init__(self, email: str, name: str, username: str, password: str, role: str):
        self.email = email
        self.username = username
        self.password = password
        self.name = name
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


class UserTriesResponse:
    def __init__(self, is_blocked: bool, try_access: UserAccessTries | None = None):
        self.is_blocked = is_blocked
        self.try_access = try_access


class UserOTPResponse:
    def __init__(self, otp: str, expiration_time: int):
        self.otp = otp
        self.expiration_time = expiration_time


class UserOTPNotificationRequest:
    def __init__(self, email: str, otp: str, expiration_time: int, username: str):
        self.email = email
        self.otp = otp
        self.expiration_time = expiration_time
        self.username = username


class UserManagerService:

    MAX_USER_ACCESS_TRY_LIMIT = int(
        EnvironmentVariablesConstants.USER_ACCESS_TRY_LIMIT
    ) + int(EnvironmentVariablesConstants.USER_ACCESS_LOCK_LIMIT)

    EMAIL_OTP_SUBJECT = "Código de verificación"
    NOTIFICATION_TEMPLATE = "otp"

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        role_repository: RoleRepository,
        notification_service: NotificationService,
        template_loader: TemplateLoader,
        otp_generator: OTPGenerator,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.role_repository = role_repository
        self.notification_service = notification_service
        self.template_loader = template_loader
        self.otp_generator = otp_generator

    async def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        """Create a new user based on the provided request data.

        Args:
            request (CreateUserRequest): Request object containing the user data for creation

        Returns:
            CreateUserResponse: Response object containing the result of the user creation process
        """
        if not EnvironmentVariablesConstants.LOGIN_URL_BASE:
            return CreateUserResponse(
                is_success=False,
                message="Login URL base is not set in environment variables",
            )

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
            name=request.name,
            password_hashed=password_hashed,
            status=UserStatus.ACTIVE,
            role=user_role,
        )
        user_entity.set_role_id(role.role_id)
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
                .replace("%LOGIN_URL%", EnvironmentVariablesConstants.LOGIN_URL_BASE)
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

    async def validate_user_block(self, user_id: str) -> UserTriesResponse:
        """Validate if user is blocked based on their access tries.

        Args:
            user_id (str): The ID of the user to check.

        Returns:
            UserTriesResponse: The response object containing the user's block status.
        """
        user_tries = await self.user_repository.get_login_try_counter(user_id)
        is_blocked = self.is_blocked_user(user_tries)
        return UserTriesResponse(
            try_access=user_tries,
            is_blocked=is_blocked,
        )

    def is_blocked_user(self, user_tries: UserAccessTries | None = None) -> bool:
        """Validate if user is blocked based on their access tries.

        Args:
            user_tries (UserAccessTries | None, optional): The user's access tries information. Defaults to None.

        Returns:
            bool: True if the user is blocked, False otherwise.
        """
        if not user_tries:
            return False
        if user_tries.definitively_blocked:
            return True
        if (
            user_tries.is_temporarily_blocked
            and user_tries.temporary_block_expiration > int(time())
        ):
            return True
        return False

    async def create_fail_try(
        self, user_id: str, user_tries: UserAccessTries | None = None
    ) -> IncrementLoginTryCounterRequest:
        """Increment number of failed login attempts for a user.

        Args:
            user_id (str): User Identifier
            user_tries (UserAccessTries | None, optional): The user's access tries information. Defaults to None.

        Returns:
            IncrementLoginTryCounterRequest: The request object representing the incremented login try counter.
        """
        if not user_tries:
            increment_request = IncrementLoginTryCounterRequest(
                user_id=user_id,
                counter=1,
                is_temporarily_blocked=False,
                temporary_block_expiration=0,
                is_definitively_blocked=False,
            )
            await self.user_repository.increment_login_try_counter(increment_request)
            return increment_request
        user_tries.retry_count += 1

        if user_tries.retry_count >= int(
            EnvironmentVariablesConstants.USER_ACCESS_TRY_LIMIT
        ):
            user_tries.is_temporarily_blocked = True
            blocked_time = int(time()) + (
                int(EnvironmentVariablesConstants.USER_ACCESS_LOCK_TIME_SECONDS)
                * user_tries.retry_count
            )
            user_tries.temporary_block_expiration = blocked_time

        increment_request = IncrementLoginTryCounterRequest(
            user_id=user_id,
            counter=user_tries.retry_count,
            is_temporarily_blocked=user_tries.is_temporarily_blocked,
            temporary_block_expiration=user_tries.temporary_block_expiration,
            is_definitively_blocked=user_tries.retry_count
            >= self.MAX_USER_ACCESS_TRY_LIMIT,
        )
        await self.user_repository.increment_login_try_counter(increment_request)

        return increment_request

    async def generate_otp(self, user_id: str) -> UserOTPResponse:
        """Generate a one-time password (OTP) for a user and save it with an expiration time.

        Args:
            user_id (str): User Identifier

        Returns:
            UserOTPResponse: The generated OTP along with its expiration time.
        """
        otp = self.otp_generator.generate_otp()
        expiration_limit = int(
            EnvironmentVariablesConstants.USER_OTP_EXPIRED_TIME_SECONDS
        )
        otp_expiration_time = int(time()) + expiration_limit
        await self.user_repository.save_user_otp(
            UserOTPRequest(
                user_id=user_id, otp=otp, expiration_time=otp_expiration_time
            )
        )
        return UserOTPResponse(otp=otp, expiration_time=expiration_limit)

    async def send_otp_notification(self, request: UserOTPNotificationRequest):
        """Send an OTP notification to the user.

        Args:
            request (UserOTPNotificationRequest): The request containing email, OTP, expiration time, and username.
        """
        notification_config_builder = NotificationConfigBuilder(
            request.email, self.EMAIL_OTP_SUBJECT
        )

        try:
            html_content = self.template_loader.load(self.NOTIFICATION_TEMPLATE)
            html_content = (
                html_content.replace("%USER%", request.username)
                .replace("%OTP_CODE%", request.otp)
                .replace("%OTP_EXPIRATION_MINUTES%", str(request.expiration_time // 60))
            )
            notification_config_builder.set_template(html_content)
            notification_config = notification_config_builder.build()

            _ = await self.notification_service.send_notification(notification_config)
        except FileNotFoundError:
            print("Email template not found. Please contact support.")
