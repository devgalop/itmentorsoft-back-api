from abc import ABC, abstractmethod
import uuid


class RefreshTokenInfo:
    """Data class to hold information about a refresh token.

    Args:
        user_id (str): The ID of the user associated with the refresh token.
        token (str): The generated refresh token (hashed before storage).
        expiration_time (float): The expiration time of the token in seconds.
        status (str): The status of the token (default is "active").
    """

    def __init__(
        self, user_id: str, token: str, expiration_time: float, status: str = "active"
    ):
        self.user_id = user_id
        self.token = token
        self.expiration_time = expiration_time
        self.status = status
        self.id_trx = uuid.uuid4().hex


class RefreshTokenData:
    def __init__(
        self, user_id: str, token_hashed: str, expiration_time: float, status: str
    ):
        self.user_id = user_id
        self.token_hashed = token_hashed
        self.expiration_time = expiration_time
        self.status = status


class TotalActiveUsers:
    def __init__(self, total_users: int):
        self.total_users = total_users


class RefreshTokenRepository(ABC):
    """Interface for refresh token repository implementations.

    Args:
        ABC (ABC): Abstract base class for refresh token repository implementations.
    """

    @abstractmethod
    async def save_token(self, info: RefreshTokenInfo):
        """Save the generated refresh token along with the associated user ID and expiration time.

        Args:
            info (RefreshTokenInfo): The information about the refresh token.
        """
        pass

    @abstractmethod
    async def get_active_token(self, user_id: str) -> RefreshTokenData | None:
        """Retrieve the active refresh token for a specific user.

        Args:
            user_id (str): The ID of the user whose active refresh token is being retrieved.

        Returns:
            RefreshTokenData: The refresh token data if found and active, otherwise None.
        """
        pass

    @abstractmethod
    async def revoke_tokens_by_user_id(self, user_id: str):
        """Revoke all refresh tokens associated with a given user ID.

        Args:
            user_id (str): The ID of the user whose tokens should be revoked.
        """
        pass

    @abstractmethod
    async def get_users_with_active_tokens(self) -> TotalActiveUsers:
        """Retrieve the total number of users with active refresh tokens.

        Returns:
            TotalActiveUsers: An object containing the total number of users with active tokens.
        """
        pass
