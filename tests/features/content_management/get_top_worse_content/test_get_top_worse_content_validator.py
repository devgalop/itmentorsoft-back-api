import pytest

from src.features.content_management.get_top_worse_content.get_top_worse_content_request import (
    GetTopWorseContentRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = GetTopWorseContentRequest(topic="python", limit=10)
    assert request.topic == "python"
    assert request.limit == 10


def test_when_topic_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="Topic cannot be empty"):
        GetTopWorseContentRequest(topic="   ", limit=10)


def test_when_topic_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="Topic must be at least 3 characters long"):
        GetTopWorseContentRequest(topic="ab", limit=10)


def test_when_topic_is_too_long_should_raise_exception():
    with pytest.raises(ValueError, match="Topic cannot exceed 100 characters"):
        GetTopWorseContentRequest(topic="a" * 101, limit=10)


def test_when_limit_is_zero_should_raise_exception():
    with pytest.raises(ValueError, match="Limit must be between 1 and 50"):
        GetTopWorseContentRequest(topic="python", limit=0)


def test_when_limit_is_negative_should_raise_exception():
    with pytest.raises(ValueError, match="Limit must be between 1 and 50"):
        GetTopWorseContentRequest(topic="python", limit=-5)


def test_when_limit_exceeds_maximum_should_raise_exception():
    with pytest.raises(ValueError, match="Limit must be between 1 and 50"):
        GetTopWorseContentRequest(topic="python", limit=51)


def test_when_limit_is_at_boundaries_should_not_raise_exception():
    request_min = GetTopWorseContentRequest(topic="python", limit=1)
    assert request_min.limit == 1

    request_max = GetTopWorseContentRequest(topic="python", limit=50)
    assert request_max.limit == 50


def test_when_limit_is_default_should_be_ten():
    request = GetTopWorseContentRequest(topic="python")
    assert request.limit == 10
