class RateLimitExceededError(Exception):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        retry_after: int,
        limit: int,
        remaining: int,
        reset: int,
        message: str = "Rate limit exceeded",
    ):
        """Initialize rate limit exceeded error.

        Args:
            retry_after: Seconds until the client can retry
            limit: Maximum requests allowed in the window
            remaining: Current remaining requests (should be 0)
            reset: Unix timestamp when the rate limit resets
            message: Error message
        """
        super().__init__(message)
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.message = message

    def __str__(self) -> str:
        return (
            f"{self.message} - retry after {self.retry_after}s, "
            f"limit: {self.limit}, remaining: {self.remaining}, "
            f"reset: {self.reset}"
        )
