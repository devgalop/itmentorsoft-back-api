import time
import logging
from dataclasses import dataclass
from typing import Optional

from src.infrastructure.cache.valkey_client import ValkeyClient
from src.infrastructure.security.rate_limiter.rate_limiter_config import RateLimitConfig
from src.infrastructure.security.rate_limiter.rate_limiter_exceptions import (
    RateLimitExceededError,
)

logger = logging.getLogger(__name__)


@dataclass
class RateLimitResult:
    """Result of a rate limit check."""

    limit: int  # Maximum requests allowed
    remaining: int  # Remaining requests in current window
    reset: int  # Unix timestamp when the window resets
    allowed: bool  # Whether the request is allowed


class RateLimiterService:
    """Service for rate limiting using token bucket algorithm with sliding window."""

    # Lua script for atomic token consumption and refill
    # This ensures no race conditions in concurrent requests
    LUA_CONSUME_TOKEN = """
    local key = KEYS[1]
    local limit = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    local block_multiplier = tonumber(ARGV[4])
    local block_duration = tonumber(ARGV[5])
    
    -- Get current state
    local data = redis.call('HMGET', key, 'tokens', 'last_refill', 'violations', 'blocked_until')
    local tokens = tonumber(data[1])
    local last_refill = tonumber(data[2])
    local violations = tonumber(data[3])
    local blocked_until = tonumber(data[4])
    
    -- Check if blocked
    if blocked_until and now < blocked_until then
        return {0, 0, blocked_until, violations or 0, 1}
    elseif blocked_until and now >= blocked_until then
        -- Block expired, reset violations
        violations = 0
        redis.call('HDEL', key, 'blocked_until')
    end
    
    -- Initialize if first request
    if not tokens then
        tokens = limit
        last_refill = now
        violations = 0
    end
    
    -- Refill tokens based on elapsed time
    local elapsed = now - last_refill
    local refill_rate = limit / window
    local tokens_to_add = elapsed * refill_rate
    tokens = math.min(limit, tokens + tokens_to_add)
    last_refill = now
    
    -- Try to consume token
    local allowed = 0
    if tokens >= 1 then
        tokens = tokens - 1
        allowed = 1
    else
        -- Track violation
        violations = (violations or 0) + 1
        
        -- Check if should block (5x limit violations in 1 hour window)
        if violations >= block_multiplier * limit then
            blocked_until = now + block_duration
            redis.call('HSET', key, 'blocked_until', blocked_until)
        end
    end
    
    -- Update state
    redis.call('HMSET', key, 
        'tokens', tokens,
        'last_refill', last_refill,
        'violations', violations
    )
    
    -- Set TTL to window + block_duration (to persist violations)
    redis.call('EXPIRE', key, window + block_duration)
    
    local reset_time = last_refill + window
    
    return {allowed, math.floor(tokens), reset_time, violations, blocked_until and 1 or 0}
    """

    def __init__(self, valkey_client: ValkeyClient):
        """Initialize rate limiter service.

        Args:
            valkey_client: Valkey/Redis client for storing rate limit data
        """
        self.valkey_client = valkey_client
        self._lua_sha: Optional[str] = None

    async def _ensure_lua_script(self) -> str | None:
        """Load Lua script into Valkey if not already loaded.

        Returns:
            str: SHA1 hash of the loaded script
        """
        if self._lua_sha is None:
            result = await self.valkey_client.client.script_load(self.LUA_CONSUME_TOKEN)
            self._lua_sha = result
        return self._lua_sha

    def _get_key(self, identifier: str, endpoint: str, scope: str) -> str:
        """Generate the Valkey key for rate limiting.

        Args:
            identifier: User ID or IP address
            endpoint: Request endpoint path
            scope: Rate limit scope (ip, user, global)

        Returns:
            str: Valkey key
        """
        if scope == "global":
            return f"rate_limit:global:{endpoint}"
        elif scope == "user":
            return f"rate_limit:user:{identifier}:{endpoint}"
        else:  # ip scope
            return f"rate_limit:ip:{identifier}:{endpoint}"

    async def check_rate_limit(
        self, identifier: str, endpoint: str, config: RateLimitConfig
    ) -> RateLimitResult:
        """Check current rate limit status without consuming a token.

        Args:
            identifier: User ID or IP address
            endpoint: Request endpoint path
            config: Rate limit configuration

        Returns:
            RateLimitResult: Current rate limit status

        Raises:
            Exception: If Valkey operation fails
        """
        key = self._get_key(identifier, endpoint, config.scope)
        now = time.time()

        try:
            # Get current state
            data = await self.valkey_client.client.hmget(
                key, "tokens", "last_refill", "blocked_until"
            )
            tokens = float(data[0]) if data[0] else config.limit
            last_refill = float(data[1]) if data[1] else now
            blocked_until = float(data[2]) if data[2] else None

            # Check if blocked
            if blocked_until and now < blocked_until:
                reset = int(blocked_until)
                return RateLimitResult(
                    limit=config.limit,
                    remaining=0,
                    reset=reset,
                    allowed=False,
                )

            # Calculate current tokens after refill
            elapsed = now - last_refill
            refill_rate = config.limit / config.window_seconds
            current_tokens = min(config.limit, tokens + elapsed * refill_rate)

            reset = int(last_refill + config.window_seconds)
            remaining = int(current_tokens)

            return RateLimitResult(
                limit=config.limit,
                remaining=remaining,
                reset=reset,
                allowed=current_tokens >= 1,
            )
        except Exception as e:
            logger.error(f"Error checking rate limit for {key}: {e}")
            raise

    async def consume_token(
        self, identifier: str, endpoint: str, config: RateLimitConfig
    ) -> bool:
        """Consume a rate limit token for the given identifier and endpoint.

        Args:
            identifier: User ID or IP address
            endpoint: Request endpoint path
            config: Rate limit configuration

        Returns:
            bool: True if token was consumed (allowed), False if rate limit exceeded

        Raises:
            Exception: If Valkey operation fails
        """
        key = self._get_key(identifier, endpoint, config.scope)
        now = time.time()

        try:
            # Execute Lua script atomically
            lua_sha = await self._ensure_lua_script()
            result = await self.valkey_client.client.evalsha(
                lua_sha,
                1,  # number of keys
                key,
                config.limit,
                config.window_seconds,
                now,
                5,  # block_multiplier
                900,  # block_duration (15 minutes)
            )

            allowed = bool(result[0])
            return allowed
        except Exception as e:
            logger.error(f"Error consuming token for {key}: {e}")
            raise

    async def is_blocked(
        self, identifier: str, endpoint: str, scope: str = "ip"
    ) -> tuple[bool, int]:
        """Check if an identifier is currently blocked.

        Args:
            identifier: User ID or IP address
            endpoint: Request endpoint path
            scope: Rate limit scope

        Returns:
            tuple[bool, int]: (is_blocked, retry_after_seconds)
        """
        key = self._get_key(identifier, endpoint, scope)
        now = time.time()

        try:
            blocked_until = await self.valkey_client.client.hget(key, "blocked_until")
            if blocked_until:
                blocked_until_ts = float(blocked_until)
                if now < blocked_until_ts:
                    retry_after = int(blocked_until_ts - now)
                    return True, retry_after
            return False, 0
        except Exception as e:
            logger.error(f"Error checking block status for {key}: {e}")
            return False, 0

    async def check_and_consume(
        self, identifier: str, endpoint: str, config: RateLimitConfig
    ) -> RateLimitResult:
        """Check rate limit and consume a token if allowed.

        This is the main method that combines checking and consuming in one operation.

        Args:
            identifier: User ID or IP address
            endpoint: Request endpoint path
            config: Rate limit configuration

        Returns:
            RateLimitResult: Result with current state after consumption

        Raises:
            RateLimitExceededError: If rate limit is exceeded
        """
        # First check if blocked
        is_blocked, retry_after = await self.is_blocked(
            identifier, endpoint, config.scope
        )
        if is_blocked:
            # Get current state for error
            result = await self.check_rate_limit(identifier, endpoint, config)
            raise RateLimitExceededError(
                retry_after=retry_after,
                limit=config.limit,
                remaining=0,
                reset=result.reset,
                message="Rate limit exceeded - temporarily blocked",
            )

        # Consume token
        allowed = await self.consume_token(identifier, endpoint, config)

        # Get updated state
        result = await self.check_rate_limit(identifier, endpoint, config)

        if not allowed:
            raise RateLimitExceededError(
                retry_after=result.reset - int(time.time()),
                limit=result.limit,
                remaining=0,
                reset=result.reset,
                message="Rate limit exceeded",
            )

        return result
