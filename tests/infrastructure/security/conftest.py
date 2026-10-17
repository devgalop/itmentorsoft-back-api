"""Shared fixtures for rate limiter tests."""

import pytest
from unittest.mock import AsyncMock

from src.infrastructure.security.rate_limiter.rate_limiter_config import RateLimitConfig


@pytest.fixture
def mock_valkey_client():
    """Create a mocked ValkeyClient with async methods.

    ValkeyClient exposes its Redis connection via .client attribute,
    so the mock must provide a .client with the actual Redis methods.
    """
    mock_redis = AsyncMock()
    mock_redis.script_load = AsyncMock()
    mock_redis.evalsha = AsyncMock()
    mock_redis.hmget = AsyncMock()
    mock_redis.hget = AsyncMock()
    mock_redis.hset = AsyncMock()
    mock_redis.hdel = AsyncMock()
    mock_redis.hmset = AsyncMock()
    mock_redis.expire = AsyncMock()

    client = AsyncMock()
    client.client = mock_redis
    return client


@pytest.fixture
def rate_limiter_service(mock_valkey_client):
    """Create a RateLimiterService with mocked ValkeyClient."""
    from src.infrastructure.security.rate_limiter.rate_limiter_service import (
        RateLimiterService,
    )

    return RateLimiterService(mock_valkey_client)


@pytest.fixture
def default_config():
    """Create a default rate limit configuration (public general)."""
    return RateLimitConfig(
        endpoint_pattern="/*",
        limit=60,
        window_seconds=60,
        scope="ip",
    )


@pytest.fixture
def login_config():
    """Create a login endpoint rate limit configuration."""
    return RateLimitConfig(
        endpoint_pattern="/users/login",
        limit=5,
        window_seconds=60,
        scope="ip",
    )


@pytest.fixture
def user_config():
    """Create a user-scoped rate limit configuration."""
    return RateLimitConfig(
        endpoint_pattern="/api/*",
        limit=100,
        window_seconds=60,
        scope="user",
    )
