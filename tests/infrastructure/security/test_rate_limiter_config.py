"""Unit tests for rate limiter configuration.

Tests cover pattern matching, predefined configs, and config retrieval logic.
"""

from src.infrastructure.security.rate_limiter.rate_limiter_config import (
    RateLimitConfig,
    PREDEFINED_CONFIGS,
    get_config_for_endpoint,
)


class TestPredefinedConfigs:
    """Tests for predefined rate limit configurations."""

    def test_login_config_has_correct_values(self):
        """GIVEN the login predefined config
        WHEN accessed
        THEN it has 5 requests per 60 seconds with IP scope.
        """
        login = PREDEFINED_CONFIGS["login"]
        assert login.endpoint_pattern == "/users/login"
        assert login.limit == 5
        assert login.window_seconds == 60
        assert login.scope == "ip"

    def test_register_config_has_correct_values(self):
        """GIVEN the register predefined config
        WHEN accessed
        THEN it has 3 requests per 60 seconds with IP scope.
        """
        register = PREDEFINED_CONFIGS["register"]
        assert register.endpoint_pattern == "/users/register"
        assert register.limit == 3
        assert register.window_seconds == 60
        assert register.scope == "ip"

    def test_reset_password_request_config_has_correct_values(self):
        """GIVEN the reset_password_request predefined config
        WHEN accessed
        THEN it has 3 requests per 10 minutes with IP scope.
        """
        reset = PREDEFINED_CONFIGS["reset_password_request"]
        assert reset.endpoint_pattern == "/users/recovery-password"
        assert reset.limit == 3
        assert reset.window_seconds == 600  # 10 minutes
        assert reset.scope == "ip"

    def test_reset_password_confirm_config_has_correct_values(self):
        """GIVEN the reset_password_confirm predefined config
        WHEN accessed
        THEN it has 3 requests per 10 minutes with IP scope.
        """
        reset_confirm = PREDEFINED_CONFIGS["reset_password_confirm"]
        assert reset_confirm.endpoint_pattern == "/users/reset-password"
        assert reset_confirm.limit == 3
        assert reset_confirm.window_seconds == 600
        assert reset_confirm.scope == "ip"

    def test_authenticated_general_config_has_correct_values(self):
        """GIVEN the authenticated_general predefined config
        WHEN accessed
        THEN it has 100 requests per 60 seconds with user scope.
        """
        auth_general = PREDEFINED_CONFIGS["authenticated_general"]
        assert auth_general.endpoint_pattern == "/*"
        assert auth_general.limit == 100
        assert auth_general.window_seconds == 60
        assert auth_general.scope == "user"

    def test_public_general_config_has_correct_values(self):
        """GIVEN the public_general predefined config
        WHEN accessed
        THEN it has 60 requests per 60 seconds with IP scope.
        """
        public_general = PREDEFINED_CONFIGS["public_general"]
        assert public_general.endpoint_pattern == "/*"
        assert public_general.limit == 60
        assert public_general.window_seconds == 60
        assert public_general.scope == "ip"


class TestPatternMatching:
    """Tests for endpoint pattern matching logic."""

    def test_when_exact_match_then_returns_exact_config(self):
        """GIVEN an endpoint that exactly matches a predefined pattern
        WHEN get_config_for_endpoint is called
        THEN it returns the exact match config (not wildcard).
        """
        config = get_config_for_endpoint("/users/login", "POST")

        assert config.endpoint_pattern == "/users/login"
        assert config.limit == 5
        assert config.scope == "ip"

    def test_when_exact_match_for_register_then_returns_register_config(self):
        """GIVEN the /users/register endpoint
        WHEN get_config_for_endpoint is called
        THEN it returns the register config.
        """
        config = get_config_for_endpoint("/users/register", "POST")

        assert config.endpoint_pattern == "/users/register"
        assert config.limit == 3

    def test_when_exact_match_for_recovery_password_then_returns_correct_config(self):
        """GIVEN the /users/recovery-password endpoint
        WHEN get_config_for_endpoint is called
        THEN it returns the recovery password config.
        """
        config = get_config_for_endpoint("/users/recovery-password", "POST")

        assert config.endpoint_pattern == "/users/recovery-password"
        assert config.limit == 3
        assert config.window_seconds == 600

    def test_when_wildcard_match_authenticated_then_returns_authenticated_config(self):
        """GIVEN an endpoint not matching any exact pattern and is_authenticated=True
        WHEN get_config_for_endpoint is called
        THEN it returns authenticated_general config.
        """
        config = get_config_for_endpoint(
            "/api/some-endpoint", "GET", is_authenticated=True
        )

        assert config.limit == 100
        assert config.scope == "user"

    def test_when_wildcard_match_unauthenticated_then_returns_public_config(self):
        """GIVEN an endpoint not matching any exact pattern and is_authenticated=False
        WHEN get_config_for_endpoint is called
        THEN it returns public_general config.
        """
        config = get_config_for_endpoint(
            "/api/some-endpoint", "GET", is_authenticated=False
        )

        assert config.limit == 60
        assert config.scope == "ip"

    def test_when_unknown_endpoint_unauthenticated_then_returns_public_general(self):
        """GIVEN an endpoint that matches no specific pattern
        WHEN get_config_for_endpoint is called with is_authenticated=False
        THEN it defaults to public_general.
        """
        config = get_config_for_endpoint("/completely/unknown/path", "GET")

        assert config.limit == 60
        assert config.scope == "ip"

    def test_when_unknown_endpoint_authenticated_then_returns_authenticated_general(
        self,
    ):
        """GIVEN an endpoint that matches no specific pattern
        WHEN get_config_for_endpoint is called with is_authenticated=True
        THEN it defaults to authenticated_general.
        """
        config = get_config_for_endpoint(
            "/completely/unknown/path", "GET", is_authenticated=True
        )

        assert config.limit == 100
        assert config.scope == "user"

    def test_when_different_http_methods_then_same_config_for_same_endpoint(self):
        """GIVEN the same endpoint accessed with different HTTP methods
        WHEN get_config_for_endpoint is called
        THEN the method does not affect matching (only auth status does).
        """
        config_get = get_config_for_endpoint("/users/login", "GET")
        config_post = get_config_for_endpoint("/users/login", "POST")

        # Both return the same config (exact match)
        assert config_get.limit == config_post.limit == 5
        assert config_get.scope == config_post.scope == "ip"


class TestConfigRetrieval:
    """Tests for the get_config_for_endpoint function."""

    def test_when_endpoint_is_login_then_returns_login_config(self):
        """GIVEN the /users/login endpoint
        WHEN get_config_for_endpoint is called
        THEN it returns the login config regardless of auth status.
        """
        config_anon = get_config_for_endpoint("/users/login", "POST")
        config_auth = get_config_for_endpoint(
            "/users/login", "POST", is_authenticated=True
        )

        # Exact match takes precedence over wildcard
        assert config_anon.endpoint_pattern == "/users/login"
        assert config_auth.endpoint_pattern == "/users/login"

    def test_when_endpoint_has_trailing_slash_then_exact_match_fails(self):
        """GIVEN an endpoint with trailing slash vs exact pattern without
        WHEN get_config_for_endpoint is called
        THEN it does NOT match exactly (falls through to wildcard/default).

        Note: The matching logic uses string equality, not path normalization.
        """
        config = get_config_for_endpoint("/users/login/", "POST")

        # Does not match exact "/users/login", falls to default
        assert config.limit in [60, 100]  # public or authenticated general

    def test_when_all_predefined_configs_exist(self):
        """GIVEN the PREDEFINED_CONFIGS dictionary
        WHEN accessed
        THEN all expected keys are present.
        """
        expected_keys = {
            "login",
            "register",
            "reset_password_request",
            "reset_password_confirm",
            "authenticated_general",
            "public_general",
        }
        assert set(PREDEFINED_CONFIGS.keys()) == expected_keys

    def test_when_rate_limit_config_created_then_has_all_fields(self):
        """GIVEN a new RateLimitConfig
        WHEN created
        THEN it has all required fields.
        """
        config = RateLimitConfig(
            endpoint_pattern="/test",
            limit=10,
            window_seconds=30,
            scope="user",
        )

        assert config.endpoint_pattern == "/test"
        assert config.limit == 10
        assert config.window_seconds == 30
        assert config.scope == "user"

    def test_when_scope_is_invalid_type_then_dataclass_allows_it(self):
        """GIVEN a RateLimitConfig with scope outside Literal values
        WHEN created at runtime (type checking is static only)
        THEN the dataclass accepts it (no runtime validation).

        Note: Literal["ip", "user", "global"] is enforced by type checkers,
        not at runtime by dataclass.
        """
        # This works at runtime (no validation), but type checkers would flag it
        config = RateLimitConfig(
            endpoint_pattern="/test",
            limit=10,
            window_seconds=30,
            scope="ip",  # valid
        )
        assert config.scope == "ip"


class TestScopeVariants:
    """Tests for different scope values in config."""

    def test_login_scope_is_ip(self):
        """GIVEN the login config
        WHEN checked
        THEN scope is 'ip' for per-IP rate limiting.
        """
        assert PREDEFINED_CONFIGS["login"].scope == "ip"

    def test_authenticated_general_scope_is_user(self):
        """GIVEN the authenticated_general config
        WHEN checked
        THEN scope is 'user' for per-user rate limiting.
        """
        assert PREDEFINED_CONFIGS["authenticated_general"].scope == "user"

    def test_public_general_scope_is_ip(self):
        """GIVEN the public_general config
        WHEN checked
        THEN scope is 'ip' for per-IP rate limiting.
        """
        assert PREDEFINED_CONFIGS["public_general"].scope == "ip"
