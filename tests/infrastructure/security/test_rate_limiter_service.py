"""Unit tests for RateLimiterService.

Tests cover token consumption, rate limit checking, progressive blocking,
concurrency handling, and edge cases.
"""

import time
import pytest

from src.infrastructure.security.rate_limiter.rate_limiter_service import (
    RateLimitResult,
)
from src.infrastructure.security.rate_limiter.rate_limiter_exceptions import (
    RateLimitExceededError,
)


class TestTokenConsumption:
    """Tests for token consumption behavior."""

    @pytest.mark.asyncio
    async def test_when_tokens_available_then_should_consume_and_return_true(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN the rate limiter has tokens available
        WHEN consume_token is called
        THEN it returns True indicating the request is allowed.
        """
        # Lua script returns: [allowed=1, tokens, reset_time, violations, is_blocked]
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [1, 59, time.time() + 60, 0, 0]

        result = await rate_limiter_service.consume_token(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert result is True
        mock_valkey_client.client.evalsha.assert_called_once()

    @pytest.mark.asyncio
    async def test_when_no_tokens_available_then_should_return_false(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN the rate limiter has zero tokens
        WHEN consume_token is called
        THEN it returns False indicating the request is denied.
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [0, 0, time.time() + 60, 1, 0]

        result = await rate_limiter_service.consume_token(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_when_window_expires_then_should_refill_tokens(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN tokens were depleted but the window has expired
        WHEN consume_token is called
        THEN tokens are refilled and the request is allowed.

        Note: The Lua script handles refill logic internally.
        This test verifies the service correctly delegates to the script.
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        # After window expires, Lua script refills and allows
        mock_valkey_client.client.evalsha.return_value = [1, 59, time.time() + 60, 0, 0]

        result = await rate_limiter_service.consume_token(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert result is True
        # Verify evalsha was called with correct arguments
        call_args = mock_valkey_client.client.evalsha.call_args
        assert call_args[0][0] == "mock_sha"  # SHA hash
        assert call_args[0][1] == 1  # number of keys

    @pytest.mark.asyncio
    async def test_when_partial_time_elapsed_then_should_refill_proportionally(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN half the window has elapsed since last refill
        WHEN consume_token is called
        THEN the Lua script handles proportional refill internally.

        Note: This is tested implicitly through the Lua script behavior.
        The service correctly passes the current timestamp to the script.
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [1, 30, time.time() + 30, 0, 0]

        result = await rate_limiter_service.consume_token(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert result is True
        # Verify current timestamp is passed to Lua script
        call_args = mock_valkey_client.client.evalsha.call_args
        now_arg = call_args[0][
            5
        ]  # ARGV[3] = now (index: sha, numkeys, key, limit, window, now)
        assert isinstance(now_arg, float)


class TestRateLimitChecking:
    """Tests for check_rate_limit method."""

    @pytest.mark.asyncio
    async def test_when_checking_rate_limit_then_should_return_correct_result(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a valid identifier and endpoint
        WHEN check_rate_limit is called
        THEN it returns a RateLimitResult with correct fields.
        """
        now = time.time()
        mock_valkey_client.client.hmget.return_value = [
            str(50),  # tokens
            str(now - 10),  # last_refill (10 seconds ago)
            None,  # not blocked
        ]

        result = await rate_limiter_service.check_rate_limit(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert isinstance(result, RateLimitResult)
        assert result.limit == 60
        assert result.remaining >= 0
        assert result.reset > now
        assert isinstance(result.allowed, bool)

    @pytest.mark.asyncio
    async def test_when_calculating_remaining_then_should_account_for_refill(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN 30 tokens remaining 10 seconds ago with 60 token limit
        WHEN check_rate_limit is called
        THEN remaining tokens are calculated with refill rate applied.
        """
        now = time.time()
        # 30 tokens, last refill 10 seconds ago
        # refill_rate = 60 / 60 = 1 token/sec
        # tokens_to_add = 10 * 1 = 10
        # current = min(60, 30 + 10) = 40
        mock_valkey_client.client.hmget.return_value = [
            str(30),  # tokens
            str(now - 10),  # last_refill
            None,
        ]

        result = await rate_limiter_service.check_rate_limit(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert result.remaining == 40

    @pytest.mark.asyncio
    async def test_when_calculating_reset_then_should_return_window_end(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a last_refill timestamp
        WHEN check_rate_limit is called
        THEN reset is calculated as last_refill + window_seconds.
        """
        now = time.time()
        last_refill = now - 20
        mock_valkey_client.client.hmget.return_value = [
            str(50),
            str(last_refill),
            None,
        ]

        result = await rate_limiter_service.check_rate_limit(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        expected_reset = int(last_refill + 60)  # window_seconds = 60
        assert result.reset == expected_reset

    @pytest.mark.asyncio
    async def test_when_no_data_exists_then_should_return_full_tokens(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN no rate limit data exists (first request)
        WHEN check_rate_limit is called
        THEN it returns full token count.
        """
        mock_valkey_client.client.hmget.return_value = [None, None, None]

        result = await rate_limiter_service.check_rate_limit(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert result.remaining == default_config.limit
        assert result.allowed is True


class TestProgressiveBlocking:
    """Tests for progressive blocking behavior."""

    @pytest.mark.asyncio
    async def test_when_exceeding_limit_5x_then_should_block(
        self, rate_limiter_service, mock_valkey_client, login_config
    ):
        """GIVEN a user has exceeded the rate limit 5 times (block_multiplier * limit)
        WHEN they attempt another request
        THEN the Lua script should block them.

        Note: The Lua script handles violation counting.
        For login (limit=5), block triggers at 5*5=25 violations.
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        # Lua script returns: [allowed=0, tokens=0, reset, violations=25, blocked=1]
        mock_valkey_client.client.evalsha.return_value = [
            0,
            0,
            time.time() + 60,
            25,
            1,
        ]

        result = await rate_limiter_service.consume_token(
            identifier="192.168.1.1",
            endpoint="/users/login",
            config=login_config,
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_when_blocked_then_should_return_correct_duration(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a user is blocked
        WHEN is_blocked is called
        THEN it returns True with the correct retry_after seconds.
        """
        now = time.time()
        blocked_until = now + 900  # 15 minutes
        mock_valkey_client.client.hget.return_value = str(blocked_until)

        is_blocked, retry_after = await rate_limiter_service.is_blocked(
            identifier="192.168.1.1",
            endpoint="/api/test",
            scope="ip",
        )

        assert is_blocked is True
        assert retry_after > 0
        assert retry_after <= 900

    @pytest.mark.asyncio
    async def test_when_block_expired_then_should_reset(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a user was blocked but the block duration has expired
        WHEN is_blocked is called
        THEN it returns False with retry_after=0.
        """
        now = time.time()
        blocked_until = now - 100  # expired 100 seconds ago
        mock_valkey_client.client.hget.return_value = str(blocked_until)

        is_blocked, retry_after = await rate_limiter_service.is_blocked(
            identifier="192.168.1.1",
            endpoint="/api/test",
            scope="ip",
        )

        assert is_blocked is False
        assert retry_after == 0

    @pytest.mark.asyncio
    async def test_when_not_blocked_then_should_return_false(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a user has no block record
        WHEN is_blocked is called
        THEN it returns False with retry_after=0.
        """
        mock_valkey_client.client.hget.return_value = None

        is_blocked, retry_after = await rate_limiter_service.is_blocked(
            identifier="192.168.1.1",
            endpoint="/api/test",
            scope="ip",
        )

        assert is_blocked is False
        assert retry_after == 0


class TestCheckAndConsume:
    """Tests for the check_and_consume method."""

    @pytest.mark.asyncio
    async def test_when_allowed_then_should_return_rate_limit_result(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a request is within rate limits
        WHEN check_and_consume is called
        THEN it returns a RateLimitResult with allowed=True.
        """
        # Mock is_blocked to return False
        mock_valkey_client.client.hget.return_value = None

        # Mock consume_token (via evalsha)
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [1, 59, time.time() + 60, 0, 0]

        # Mock check_rate_limit (via hmget)
        now = time.time()
        mock_valkey_client.client.hmget.return_value = [
            str(59),
            str(now),
            None,
        ]

        result = await rate_limiter_service.check_and_consume(
            identifier="192.168.1.1",
            endpoint="/api/test",
            config=default_config,
        )

        assert isinstance(result, RateLimitResult)
        assert result.limit == 60

    @pytest.mark.asyncio
    async def test_when_blocked_then_should_raise_rate_limit_exceeded_error(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a user is blocked
        WHEN check_and_consume is called
        THEN it raises RateLimitExceededError with retry_after.
        """
        now = time.time()
        blocked_until = now + 900
        mock_valkey_client.client.hget.return_value = str(blocked_until)

        # Mock check_rate_limit for error details
        mock_valkey_client.client.hmget.return_value = [
            str(0),
            str(now),
            str(blocked_until),
        ]

        with pytest.raises(RateLimitExceededError) as exc_info:
            await rate_limiter_service.check_and_consume(
                identifier="192.168.1.1",
                endpoint="/api/test",
                config=default_config,
            )

        assert exc_info.value.retry_after > 0
        assert exc_info.value.remaining == 0

    @pytest.mark.asyncio
    async def test_when_tokens_exhausted_then_should_raise_rate_limit_exceeded_error(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN a user has no tokens remaining
        WHEN check_and_consume is called
        THEN it raises RateLimitExceededError.
        """
        # Not blocked
        mock_valkey_client.client.hget.return_value = None

        # consume_token returns False (no tokens)
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [0, 0, time.time() + 60, 1, 0]

        # check_rate_limit returns 0 remaining
        now = time.time()
        mock_valkey_client.client.hmget.return_value = [
            str(0),
            str(now),
            None,
        ]

        with pytest.raises(RateLimitExceededError) as exc_info:
            await rate_limiter_service.check_and_consume(
                identifier="192.168.1.1",
                endpoint="/api/test",
                config=default_config,
            )

        assert exc_info.value.remaining == 0


class TestConcurrencyAndAtomicity:
    """Tests for concurrent request handling."""

    @pytest.mark.asyncio
    async def test_when_concurrent_requests_then_lua_script_ensures_atomicity(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN multiple concurrent requests
        WHEN consume_token is called concurrently
        THEN the Lua script ensures atomic token consumption.

        Note: This test verifies the service correctly delegates to the Lua script.
        The actual atomicity is guaranteed by Redis/Valkey's Lua script execution.
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        # All requests go through evalsha (Lua script)
        mock_valkey_client.client.evalsha.return_value = [1, 58, time.time() + 60, 0, 0]

        # Simulate 3 concurrent requests
        import asyncio

        tasks = [
            rate_limiter_service.consume_token(
                "192.168.1.1", "/api/test", default_config
            )
            for _ in range(3)
        ]
        results = await asyncio.gather(*tasks)

        # All should succeed (in real scenario, tokens would decrement)
        assert all(r is True for r in results)
        # Verify evalsha was called 3 times (once per request)
        assert mock_valkey_client.client.evalsha.call_count == 3


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_when_valkey_fails_then_should_raise_exception(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN Valkey connection fails
        WHEN consume_token is called
        THEN it raises an exception.
        """
        mock_valkey_client.client.script_load.side_effect = Exception(
            "Connection failed"
        )

        with pytest.raises(Exception):
            await rate_limiter_service.consume_token(
                identifier="192.168.1.1",
                endpoint="/api/test",
                config=default_config,
            )

    @pytest.mark.asyncio
    async def test_when_identifier_is_empty_then_should_still_generate_key(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN an empty identifier
        WHEN consume_token is called
        THEN it generates a key with empty identifier (not ideal but handled).
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [1, 59, time.time() + 60, 0, 0]

        result = await rate_limiter_service.consume_token(
            identifier="",
            endpoint="/api/test",
            config=default_config,
        )

        # Should not crash, though empty identifier is not ideal
        assert result is True

    @pytest.mark.asyncio
    async def test_when_scope_is_user_then_key_includes_user_id(
        self, rate_limiter_service, mock_valkey_client, user_config
    ):
        """GIVEN a user-scoped config
        WHEN consume_token is called
        THEN the key includes the user identifier.
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [1, 99, time.time() + 60, 0, 0]

        await rate_limiter_service.consume_token(
            identifier="user-123",
            endpoint="/api/test",
            config=user_config,
        )

        # Verify the key contains "user" and the identifier
        call_args = mock_valkey_client.client.evalsha.call_args
        key = call_args[0][2]  # KEYS[1]
        assert "user" in key
        assert "user-123" in key

    @pytest.mark.asyncio
    async def test_when_scope_is_ip_then_key_includes_ip(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN an IP-scoped config
        WHEN consume_token is called
        THEN the key includes the IP address.
        """
        mock_valkey_client.client.script_load.return_value = "mock_sha"
        mock_valkey_client.client.evalsha.return_value = [1, 59, time.time() + 60, 0, 0]

        await rate_limiter_service.consume_token(
            identifier="192.168.1.100",
            endpoint="/api/test",
            config=default_config,
        )

        call_args = mock_valkey_client.client.evalsha.call_args
        key = call_args[0][2]  # KEYS[1]
        assert "ip" in key
        assert "192.168.1.100" in key

    @pytest.mark.asyncio
    async def test_when_lua_script_not_loaded_then_should_load_once(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN the Lua script has not been loaded yet
        WHEN consume_token is called multiple times
        THEN script_load is called only once (cached).
        """
        mock_valkey_client.client.script_load.return_value = "cached_sha"
        mock_valkey_client.client.evalsha.return_value = [1, 59, time.time() + 60, 0, 0]

        # Call consume_token 3 times
        for _ in range(3):
            await rate_limiter_service.consume_token(
                "192.168.1.1", "/api/test", default_config
            )

        # script_load should be called only once
        assert mock_valkey_client.client.script_load.call_count == 1

    @pytest.mark.asyncio
    async def test_when_check_rate_limit_valkey_fails_then_should_raise(
        self, rate_limiter_service, mock_valkey_client, default_config
    ):
        """GIVEN Valkey fails during check_rate_limit
        WHEN check_rate_limit is called
        THEN it raises an exception.
        """
        mock_valkey_client.client.hmget.side_effect = Exception("Connection timeout")

        with pytest.raises(Exception):
            await rate_limiter_service.check_rate_limit(
                identifier="192.168.1.1",
                endpoint="/api/test",
                config=default_config,
            )
