import logging
from typing import Optional

import jwt
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.i18n import t
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants
from src.infrastructure.security.rate_limiter.rate_limiter_config import (
    get_config_for_endpoint,
)
from src.infrastructure.security.rate_limiter.rate_limiter_exceptions import (
    RateLimitExceededError,
)
from src.infrastructure.security.rate_limiter.rate_limiter_service import (
    RateLimiterService,
)

logger = logging.getLogger(__name__)


class RateLimitEnvVars:
    """Environment variables for rate limiting configuration."""

    RATE_LIMIT_ENABLED: bool = (
        EnvironmentVariablesConstants.RATE_LIMIT_ENABLED == "true"
    )
    RATE_LIMIT_DEFAULT_LIMIT: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_DEFAULT_LIMIT
    )
    RATE_LIMIT_DEFAULT_WINDOW: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_DEFAULT_WINDOW
    )
    RATE_LIMIT_LOGIN_LIMIT: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_LOGIN_LIMIT
    )
    RATE_LIMIT_LOGIN_WINDOW: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_LOGIN_WINDOW
    )
    RATE_LIMIT_REGISTER_LIMIT: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_REGISTER_LIMIT
    )
    RATE_LIMIT_REGISTER_WINDOW: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_REGISTER_WINDOW
    )
    RATE_LIMIT_BLOCK_MULTIPLIER: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_BLOCK_MULTIPLIER
    )
    RATE_LIMIT_BLOCK_DURATION: int = int(
        EnvironmentVariablesConstants.RATE_LIMIT_BLOCK_DURATION
    )
    RATE_LIMIT_WHITELIST_IPS: list[str] = [
        ip.strip()
        for ip in EnvironmentVariablesConstants.RATE_LIMIT_WHITELIST_IPS.split(",")
        if ip.strip()
    ]
    RATE_LIMIT_EXCLUDED_PATHS: list[str] = [
        path.strip()
        for path in EnvironmentVariablesConstants.RATE_LIMIT_EXCLUDED_PATHS.split(",")
        if path.strip()
    ]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting API requests."""

    def __init__(self, app, rate_limiter: RateLimiterService, config: RateLimitEnvVars):
        """Initialize rate limit middleware.

        Args:
            app: FastAPI application instance
            rate_limiter: RateLimiterService instance
            config: Rate limit configuration from environment
        """
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.config = config

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process the request and apply rate limiting.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            Response: HTTP response
        """
        # Skip rate limiting if disabled
        if not self.config.RATE_LIMIT_ENABLED:
            return await call_next(request)

        # Skip rate limiting for excluded paths
        if self._is_excluded_path(request.url.path):
            return await call_next(request)

        # Skip rate limiting for whitelisted IPs
        client_ip = self._get_client_ip(request)
        if client_ip in self.config.RATE_LIMIT_WHITELIST_IPS:
            return await call_next(request)

        try:
            # Extract identifier (user_id or IP)
            identifier = self._extract_user_id(request) or client_ip
            is_authenticated = self._extract_user_id(request) is not None

            # Get rate limit config for this endpoint
            rate_limit_config = get_config_for_endpoint(
                request.url.path, request.method, is_authenticated
            )

            # Check and consume token
            result = await self.rate_limiter.check_and_consume(
                identifier=identifier,
                endpoint=request.url.path,
                config=rate_limit_config,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers to response
            response.headers["X-RateLimit-Limit"] = str(result.limit)
            response.headers["X-RateLimit-Remaining"] = str(result.remaining)
            response.headers["X-RateLimit-Reset"] = str(result.reset)

            return response

        except RateLimitExceededError as e:
            # Rate limit exceeded - return 429
            return JSONResponse(
                status_code=429,
                content={
                    "status": 429,
                    "message": t("error.rate_limit_exceeded"),
                    "path": request.url.path,
                },
                headers={
                    "X-RateLimit-Limit": str(e.limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(e.reset),
                    "Retry-After": str(e.retry_after),
                },
            )

        except Exception as e:
            # Graceful degradation: if Valkey fails, allow the request
            logger.error(
                f"Rate limiting error for {request.url.path}: {e}. "
                f"Allowing request due to cache failure."
            )
            return await call_next(request)

    def _is_excluded_path(self, path: str) -> bool:
        """Check if the path should be excluded from rate limiting.

        Args:
            path: Request path

        Returns:
            bool: True if path is excluded
        """
        return path in self.config.RATE_LIMIT_EXCLUDED_PATHS

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request.

        Handles X-Forwarded-For header for requests behind a proxy.

        Args:
            request: HTTP request

        Returns:
            str: Client IP address
        """
        # Check X-Forwarded-For (take first IP if behind trusted proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _extract_user_id(self, request: Request) -> Optional[str]:
        """Extract user ID from JWT token in Authorization header.

        Decodes JWT without full validation (just extracts sub claim).
        Full validation happens in endpoint dependencies.

        Args:
            request: HTTP request

        Returns:
            Optional[str]: User ID if found, None otherwise
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        try:
            token = auth_header.split(" ")[1]
            # Decode without signature verification (just extract claims)
            payload = jwt.decode(
                token,
                options={"verify_signature": False},
                algorithms=["HS256", "HS384", "HS512"],
            )
            # Try user_id first (project uses user_id), fallback to sub
            return payload.get("user_id") or payload.get("sub")
        except Exception:
            return None
