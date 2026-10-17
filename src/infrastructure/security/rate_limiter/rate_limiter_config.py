from dataclasses import dataclass
from typing import Literal


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting on a specific endpoint pattern."""

    endpoint_pattern: str  # Supports wildcards: /users/*, exact: /users/login
    limit: int  # Max requests in window
    window_seconds: int  # Time window in seconds
    scope: Literal["ip", "user", "global"]  # Scope for rate limiting


# Predefined configurations for sensitive endpoints
PREDEFINED_CONFIGS = {
    "login": RateLimitConfig(
        endpoint_pattern="/users/login",
        limit=5,
        window_seconds=60,
        scope="ip",
    ),
    "register": RateLimitConfig(
        endpoint_pattern="/users/register",
        limit=3,
        window_seconds=60,
        scope="ip",
    ),
    "reset_password_request": RateLimitConfig(
        endpoint_pattern="/users/recovery-password",
        limit=3,
        window_seconds=600,  # 10 minutes
        scope="ip",
    ),
    "reset_password_confirm": RateLimitConfig(
        endpoint_pattern="/users/reset-password",
        limit=3,
        window_seconds=600,  # 10 minutes
        scope="ip",
    ),
    "authenticated_general": RateLimitConfig(
        endpoint_pattern="/*",  # Wildcard for all authenticated endpoints
        limit=100,
        window_seconds=60,
        scope="user",
    ),
    "public_general": RateLimitConfig(
        endpoint_pattern="/*",  # Wildcard for all public endpoints
        limit=60,
        window_seconds=60,
        scope="ip",
    ),
}


def get_config_for_endpoint(
    endpoint: str, method: str, is_authenticated: bool = False
) -> RateLimitConfig:
    """Get the appropriate rate limit configuration for an endpoint.

    Args:
        endpoint: The request path (e.g., /users/login)
        method: HTTP method (GET, POST, etc.)
        is_authenticated: Whether the request has valid authentication

    Returns:
        RateLimitConfig: The matching configuration for this endpoint

    Matching logic:
        1. Exact match first (most specific)
        2. Wildcard match (less specific)
        3. Default to authenticated or public general config
    """
    # Exact match first
    for config in PREDEFINED_CONFIGS.values():
        if config.endpoint_pattern == endpoint:
            return config

    # Wildcard match
    for config in PREDEFINED_CONFIGS.values():
        if config.endpoint_pattern.endswith("/*"):
            prefix = config.endpoint_pattern[:-2]  # Remove /*
            if endpoint.startswith(prefix):
                # Return authenticated or public based on auth status
                if is_authenticated and config.scope == "user":
                    return config
                elif not is_authenticated and config.scope == "ip":
                    return config

    # Default to authenticated or public general
    if is_authenticated:
        return PREDEFINED_CONFIGS["authenticated_general"]
    return PREDEFINED_CONFIGS["public_general"]
