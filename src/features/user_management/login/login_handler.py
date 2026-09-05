from src.features.user_management.login.login_request import LoginRequest
from src.features.user_management.login.login_response import LoginResponse
from src.features.user_management.shared.password_hasher import PasswordHasher
from itmentorsoft_persistence.repositories import (
    RefreshTokenInfo,
    RefreshTokenRepository,
)
from src.features.user_management.shared.token_generator import (
    TokenGenerator,
    TokenRequest,
)
from itmentorsoft_persistence.repositories import UserRepository


class LoginHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator
        self.refresh_token_repository = refresh_token_repository

    async def handle(self, request: LoginRequest) -> LoginResponse:
        """ "Handle the login request.

        Args:
            request (LoginRequest): The login request containing the user's email and password.
        Returns:
            LoginResponse: The response indicating whether the login was successful, along with a token and its expiration time if successful.
        """

        user = await self.user_repository.get_user_by_email(request.email)
        if not user:
            return LoginResponse(
                is_successful=False, token="", expiration_time=0, user_id=None
            )  # nosec

        if not self.password_hasher.verify_password(
            request.password, user.password_hashed
        ):
            return LoginResponse(
                is_successful=False, token="", expiration_time=0, user_id=None
            )  # nosec

        token_response = self.token_generator.generate_token(
            TokenRequest(user_id=user.id, user_name=user.username, role=user.role.value)
        )

        refresh_token_response = self.token_generator.generate_random_token()
        hashed_refresh_token = self.password_hasher.hash_password(
            refresh_token_response.token
        )
        refresh_token_info = RefreshTokenInfo(
            user_id=user.id,
            token=hashed_refresh_token,
            expiration_time=refresh_token_response.expiration_time,
            status="active",
        )
        await self.refresh_token_repository.revoke_tokens_by_user_id(user.id)
        await self.refresh_token_repository.save_token(refresh_token_info)

        return LoginResponse(
            is_successful=True,
            token=token_response.token,
            expiration_time=token_response.expiration_time,
            refresh_token=refresh_token_response.token,
            user_id=user.id,
        )
