from enum import Enum
import uuid


class UserStatus(Enum):
    """User status

    Args:
        Enum (Enum): Enum class for user status.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class UserRole(Enum):
    """User role

    Args:
        Enum (Enum): Enum class for user role.
    """

    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"
    USER = "user"


class User:
    """Represents a system user

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password_hashed (str): The hashed password of the user.
        status (UserStatus): The status of the user.
        role (UserRole): The role of the user.
    """

    def __init__(
        self,
        username: str,
        email: str,
        name: str,
        password_hashed: str,
        status: UserStatus,
        role: UserRole,
    ):
        self.id = uuid.uuid4().hex
        self.username = username
        self.email = email
        self.name = name
        self.password_hashed = password_hashed
        self.status = status
        self.role = role
        self.role_id = ""

    def is_active(self) -> bool:
        """Validate if the user is active

        Returns:
            bool: True if the user is active, False otherwise.
        """
        return self.status == UserStatus.ACTIVE

    def is_admin(self) -> bool:
        """Validate if the user is an admin

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self.role == UserRole.ADMIN

    def deactivate(self):
        """Deactivate the user"""
        self.status = UserStatus.INACTIVE

    def suspend(self):
        """Suspend the user"""
        self.status = UserStatus.SUSPENDED

    def set_role_id(self, role_id: str):
        """Set the role id for the user

        Args:
            role_id (str): The role id to set for the user.
        """
        self.role_id = role_id


class CompleteUserResponse:
    """Represents a complete user response object

    Args:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        password_hashed (str): The hashed password of the user.
        status (UserStatus): The status of the user.
        role (UserRole): The role of the user.
    """

    def __init__(
        self,
        id: str,
        username: str,
        email: str,
        password_hashed: str,
        status: UserStatus,
        role: UserRole,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hashed = password_hashed
        self.status = status
        self.role = role


class UserResponse:
    """Represents a user response object

    Args:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        status (UserStatus): The status of the user.
        name (str): The name of the user.
        role (UserRole): The role of the user.
    """

    def __init__(
        self,
        id: str,
        username: str,
        email: str,
        name: str,
        status: UserStatus,
        role: UserRole,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.status = status
        self.role = role
