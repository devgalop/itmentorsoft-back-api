"""Unit tests for RateLimitMiddleware.

Tests cover middleware skip conditions, identifier extraction, successful request
handling, rate limit exceeded responses, graceful degradation, and helper methods.
"""

import time
import jwt
from unittest.mock import AsyncMock, Mock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse

from src.infrastructure.security.rate_limit_middleware import RateLimitMiddleware
from src.infrastructure.security.rate_limiter.rate_limiter_service import (
    RateLimitResult,
)
from src.infrastructure.security.rate_limiter.rate_limiter_exceptions import (
    RateLimitExceededError,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(**overrides) -> Mock:
    """Create a mocked RateLimitEnvVars config with sensible defaults."""
    config = Mock()
    config.RATE_LIMIT_ENABLED = overrides.get("enabled", True)
    config.RATE_LIMIT_WHITELIST_IPS = overrides.get("whitelist_ips", [])
    config.RATE_LIMIT_EXCLUDED_PATHS = overrides.get(
        "excluded_paths", ["/health", "/docs", "/openapi.json"]
    )
    return config


def _make_result(**overrides) -> RateLimitResult:
    """Create a RateLimitResult with defaults."""
    return RateLimitResult(
        limit=overrides.get("limit", 60),
        remaining=overrides.get("remaining", 59),
        reset=overrides.get("reset", int(time.time()) + 60),
        allowed=overrides.get("allowed", True),
    )


def _make_jwt(payload: dict) -> str:
    """Encode a JWT payload (unsigned) for testing."""
    # Use a 32-byte key to satisfy RFC 7518 minimum length for HS256
    return jwt.encode(payload, key="a" * 32, algorithm="HS256")


def _create_test_app(rate_limiter_mock: AsyncMock, config_mock: Mock) -> FastAPI:
    """Build a minimal FastAPI app wired with RateLimitMiddleware."""
    app = FastAPI()

    @app.get("/api/test")
    async def test_endpoint():
        return JSONResponse({"status": "ok"})

    @app.get("/health")
    async def health():
        return JSONResponse({"status": "healthy"})

    @app.get("/docs")
    async def docs():
        return JSONResponse({"page": "docs"})

    @app.get("/openapi.json")
    async def openapi():
        return JSONResponse({"openapi": "3.0"})

    app.add_middleware(
        RateLimitMiddleware,
        rate_limiter=rate_limiter_mock,
        config=config_mock,
    )
    return app


def _get_client(rate_limiter_mock: AsyncMock, config_mock: Mock) -> TestClient:
    """Return a TestClient for the test app."""
    app = _create_test_app(rate_limiter_mock, config_mock)
    return TestClient(app)


# ---------------------------------------------------------------------------
# TestMiddlewareSkips
# ---------------------------------------------------------------------------


class TestMiddlewareSkips:
    """Tests for middleware skip conditions (disabled, excluded paths, whitelist)."""

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_rate_limit_disabled_then_should_skip(self, mock_get_config):
        """GIVEN rate limiting is disabled via config
        WHEN any request is made
        THEN the request passes through without calling the rate limiter.
        """
        rate_limiter = AsyncMock()
        config = _make_config(enabled=False)
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.status_code == 200
        rate_limiter.check_and_consume.assert_not_called()

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_path_is_excluded_health_then_should_skip(self, mock_get_config):
        """GIVEN /health is in the excluded paths list
        WHEN a request hits /health
        THEN the rate limiter is bypassed.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/health")

        assert response.status_code == 200
        rate_limiter.check_and_consume.assert_not_called()

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_path_is_excluded_docs_then_should_skip(self, mock_get_config):
        """GIVEN /docs is in the excluded paths list
        WHEN a request hits /docs
        THEN the rate limiter is bypassed.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/docs")

        assert response.status_code == 200
        rate_limiter.check_and_consume.assert_not_called()

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_path_is_excluded_openapi_then_should_skip(self, mock_get_config):
        """GIVEN /openapi.json is in the excluded paths list
        WHEN a request hits /openapi.json
        THEN the rate limiter is bypassed.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/openapi.json")

        assert response.status_code == 200
        rate_limiter.check_and_consume.assert_not_called()

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_ip_is_whitelisted_then_should_skip(self, mock_get_config):
        """GIVEN the client IP is in the whitelist
        WHEN a request is made from that IP
        THEN the rate limiter is bypassed.

        Note: TestClient sets request.client.host to 'testclient' by default.
        We can override it via the 'client' param on TestClient.
        """
        rate_limiter = AsyncMock()
        config = _make_config(whitelist_ips=["10.0.0.1"])
        app = _create_test_app(rate_limiter, config)
        # Use explicit client IP to avoid relying on TestClient's default hostname
        client = TestClient(app, headers={"X-Forwarded-For": "10.0.0.1"})

        response = client.get("/api/test")

        assert response.status_code == 200
        rate_limiter.check_and_consume.assert_not_called()


# ---------------------------------------------------------------------------
# TestIdentifierExtraction
# ---------------------------------------------------------------------------


class TestIdentifierExtraction:
    """Tests for how the middleware extracts the rate-limit identifier."""

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_no_auth_header_then_should_use_client_ip(self, mock_get_config):
        """GIVEN an anonymous request with no Authorization header
        WHEN the middleware processes the request
        THEN the rate limiter is called with the client IP as identifier.
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.return_value = _make_result()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        # Use X-Forwarded-For to inject a known IP (TestClient default host is 'testclient')
        client.get("/api/test", headers={"X-Forwarded-For": "192.168.1.100"})

        call_kwargs = rate_limiter.check_and_consume.call_args
        identifier = call_kwargs.kwargs.get("identifier") or call_kwargs[1].get(
            "identifier"
        )
        assert identifier == "192.168.1.100"

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_valid_bearer_token_then_should_use_user_id(self, mock_get_config):
        """GIVEN a valid Bearer JWT with a user_id claim
        WHEN the middleware processes the request
        THEN the rate limiter is called with user_id as identifier.
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.return_value = _make_result()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        token = _make_jwt({"user_id": "user-42", "sub": "fallback-sub"})
        response = client.get("/api/test", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        call_kwargs = rate_limiter.check_and_consume.call_args
        identifier = call_kwargs.kwargs.get("identifier") or call_kwargs[1].get(
            "identifier"
        )
        assert identifier == "user-42"

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_jwt_has_sub_claim_then_should_use_sub(self, mock_get_config):
        """GIVEN a JWT with no user_id but with a sub claim
        WHEN the middleware processes the request
        THEN the rate limiter uses sub as identifier.
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.return_value = _make_result()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        token = _make_jwt({"sub": "sub-user-99"})
        client.get("/api/test", headers={"Authorization": f"Bearer {token}"})

        call_kwargs = rate_limiter.check_and_consume.call_args
        identifier = call_kwargs.kwargs.get("identifier") or call_kwargs[1].get(
            "identifier"
        )
        assert identifier == "sub-user-99"

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_invalid_jwt_then_should_fallback_to_ip(self, mock_get_config):
        """GIVEN a malformed Bearer token that cannot be decoded
        WHEN the middleware processes the request
        THEN it falls back to the client IP without crashing.
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.return_value = _make_result()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        # Use X-Forwarded-For to inject a known IP (TestClient default host is 'testclient')
        response = client.get(
            "/api/test",
            headers={
                "Authorization": "Bearer not.a.valid.jwt",
                "X-Forwarded-For": "192.168.1.100",
            },
        )

        assert response.status_code == 200
        call_kwargs = rate_limiter.check_and_consume.call_args
        identifier = call_kwargs.kwargs.get("identifier") or call_kwargs[1].get(
            "identifier"
        )
        assert identifier == "192.168.1.100"

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_x_forwarded_for_present_then_should_use_first_ip(
        self, mock_get_config
    ):
        """GIVEN the request has X-Forwarded-For with multiple IPs
        WHEN the middleware extracts the client IP
        THEN it uses the first IP in the list.
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.return_value = _make_result()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        client.get(
            "/api/test",
            headers={"X-Forwarded-For": "203.0.113.50, 70.41.3.18, 150.172.238.178"},
        )

        call_kwargs = rate_limiter.check_and_consume.call_args
        identifier = call_kwargs.kwargs.get("identifier") or call_kwargs[1].get(
            "identifier"
        )
        assert identifier == "203.0.113.50"


# ---------------------------------------------------------------------------
# TestSuccessfulRequests
# ---------------------------------------------------------------------------


class TestSuccessfulRequests:
    """Tests for successful (allowed) request handling and response headers."""

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_allowed_then_should_add_rate_limit_headers(self, mock_get_config):
        """GIVEN the rate limiter allows the request
        WHEN the response is returned
        THEN it includes X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset.
        """
        rate_limiter = AsyncMock()
        reset_time = int(time.time()) + 60
        rate_limiter.check_and_consume.return_value = _make_result(
            limit=100, remaining=99, reset=reset_time
        )
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.headers["X-RateLimit-Limit"] == "100"
        assert response.headers["X-RateLimit-Remaining"] == "99"
        assert response.headers["X-RateLimit-Reset"] == str(reset_time)

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_allowed_then_should_return_200(self, mock_get_config):
        """GIVEN the rate limiter allows the request
        WHEN the response is returned
        THEN the original 200 status code is preserved.
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.return_value = _make_result()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.status_code == 200

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_allowed_then_should_return_original_body(self, mock_get_config):
        """GIVEN the rate limiter allows the request
        WHEN the response is returned
        THEN the original response body is unchanged.
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.return_value = _make_result()
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# TestRateLimitExceeded
# ---------------------------------------------------------------------------


class TestRateLimitExceeded:
    """Tests for rate limit exceeded (429) responses."""

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    @patch("src.infrastructure.security.rate_limit_middleware.t")
    def test_when_rate_limit_exceeded_then_should_return_429(
        self, mock_t, mock_get_config
    ):
        """GIVEN the rate limiter raises RateLimitExceededError
        WHEN the middleware catches it
        THEN it returns a 429 status code.
        """
        mock_t.return_value = "Rate limit exceeded"
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.side_effect = RateLimitExceededError(
            retry_after=30, limit=60, remaining=0, reset=int(time.time()) + 60
        )
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.status_code == 429

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    @patch("src.infrastructure.security.rate_limit_middleware.t")
    def test_when_rate_limit_exceeded_then_should_include_retry_after_header(
        self, mock_t, mock_get_config
    ):
        """GIVEN the rate limiter raises RateLimitExceededError with retry_after=45
        WHEN the 429 response is returned
        THEN the Retry-After header equals 45.
        """
        mock_t.return_value = "Rate limit exceeded"
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.side_effect = RateLimitExceededError(
            retry_after=45, limit=60, remaining=0, reset=int(time.time()) + 60
        )
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.headers["Retry-After"] == "45"

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    @patch("src.infrastructure.security.rate_limit_middleware.t")
    def test_when_rate_limit_exceeded_then_should_include_rate_limit_headers(
        self, mock_t, mock_get_config
    ):
        """GIVEN the rate limiter raises RateLimitExceededError
        WHEN the 429 response is returned
        THEN it includes X-RateLimit-Limit, X-RateLimit-Remaining, and X-RateLimit-Reset.
        """
        mock_t.return_value = "Rate limit exceeded"
        reset_time = int(time.time()) + 60
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.side_effect = RateLimitExceededError(
            retry_after=30, limit=60, remaining=0, reset=reset_time
        )
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.headers["X-RateLimit-Limit"] == "60"
        assert response.headers["X-RateLimit-Remaining"] == "0"
        assert response.headers["X-RateLimit-Reset"] == str(reset_time)

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    @patch("src.infrastructure.security.rate_limit_middleware.t")
    def test_when_rate_limit_exceeded_then_should_return_error_body(
        self, mock_t, mock_get_config
    ):
        """GIVEN the rate limiter raises RateLimitExceededError
        WHEN the 429 response is returned
        THEN the JSON body contains status, message, and path fields.
        """
        mock_t.return_value = "Rate limit exceeded"
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.side_effect = RateLimitExceededError(
            retry_after=30, limit=60, remaining=0, reset=int(time.time()) + 60
        )
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")
        body = response.json()

        assert body["status"] == 429
        assert "message" in body
        assert body["path"] == "/api/test"


# ---------------------------------------------------------------------------
# TestGracefulDegradation
# ---------------------------------------------------------------------------


class TestGracefulDegradation:
    """Tests for graceful degradation when the rate limiter backend fails."""

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_valkey_fails_then_should_allow_request(self, mock_get_config):
        """GIVEN the rate limiter raises an unexpected Exception (e.g. Valkey down)
        WHEN the middleware catches it
        THEN the request is allowed through (graceful degradation).
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.side_effect = Exception(
            "Valkey connection refused"
        )
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    @patch("src.infrastructure.security.rate_limit_middleware.get_config_for_endpoint")
    def test_when_valkey_fails_then_should_not_add_rate_limit_headers(
        self, mock_get_config
    ):
        """GIVEN the rate limiter raises an unexpected Exception
        WHEN the middleware allows the request through
        THEN no X-RateLimit-* headers are added (best effort).
        """
        rate_limiter = AsyncMock()
        rate_limiter.check_and_consume.side_effect = Exception("Valkey timeout")
        config = _make_config()
        client = _get_client(rate_limiter, config)

        response = client.get("/api/test")

        assert "X-RateLimit-Limit" not in response.headers
        assert "X-RateLimit-Remaining" not in response.headers
        assert "X-RateLimit-Reset" not in response.headers


# ---------------------------------------------------------------------------
# TestHelperMethods
# ---------------------------------------------------------------------------


class TestHelperMethods:
    """Tests for private helper methods (_is_excluded_path, _get_client_ip)."""

    def test_when_path_matches_excluded_then_returns_true(self):
        """GIVEN _is_excluded_path is called with a path in the excluded list
        WHEN the path is /health
        THEN it returns True.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        middleware = RateLimitMiddleware(
            app=FastAPI(), rate_limiter=rate_limiter, config=config
        )

        assert middleware._is_excluded_path("/health") is True

    def test_when_path_not_excluded_then_returns_false(self):
        """GIVEN _is_excluded_path is called with a path not in the excluded list
        WHEN the path is /api/test
        THEN it returns False.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        middleware = RateLimitMiddleware(
            app=FastAPI(), rate_limiter=rate_limiter, config=config
        )

        assert middleware._is_excluded_path("/api/test") is False

    def test_when_x_forwarded_for_single_ip_then_returns_it(self):
        """GIVEN X-Forwarded-For contains a single IP
        WHEN _get_client_ip is called
        THEN it returns that IP.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        middleware = RateLimitMiddleware(
            app=FastAPI(), rate_limiter=rate_limiter, config=config
        )

        request = Mock()
        request.headers = {"X-Forwarded-For": "203.0.113.50"}

        assert middleware._get_client_ip(request) == "203.0.113.50"

    def test_when_x_forwarded_for_multiple_ips_then_returns_first(self):
        """GIVEN X-Forwarded-For contains multiple comma-separated IPs
        WHEN _get_client_ip is called
        THEN it returns the first (leftmost) IP, stripped.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        middleware = RateLimitMiddleware(
            app=FastAPI(), rate_limiter=rate_limiter, config=config
        )

        request = Mock()
        request.headers = {
            "X-Forwarded-For": "203.0.113.50, 70.41.3.18, 150.172.238.178"
        }

        assert middleware._get_client_ip(request) == "203.0.113.50"

    def test_when_no_x_forwarded_for_then_returns_client_host(self):
        """GIVEN no X-Forwarded-For header is present
        WHEN _get_client_ip is called
        THEN it returns request.client.host.
        """
        rate_limiter = AsyncMock()
        config = _make_config()
        middleware = RateLimitMiddleware(
            app=FastAPI(), rate_limiter=rate_limiter, config=config
        )

        request = Mock()
        request.headers = {}
        request.client = Mock()
        request.client.host = "192.168.1.42"

        assert middleware._get_client_ip(request) == "192.168.1.42"
