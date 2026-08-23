import pytest

from src.features.content_management.update_content_path_status.update_content_path_status_request import (
    UpdateContentPathStatusRequest,
)


def test_when_all_fields_are_valid_should_not_raise():
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=True
    )
    assert request.path_id == "path_123"
    assert request.content_id == "content_456"
    assert request.status is True


def test_when_path_id_is_empty_should_raise():
    with pytest.raises(ValueError, match="path_id must not be empty"):
        UpdateContentPathStatusRequest(
            path_id="", content_id="content_456", status=True
        )


def test_when_path_id_is_too_short_should_raise():
    with pytest.raises(ValueError, match="path_id must be at least 5 characters long"):
        UpdateContentPathStatusRequest(
            path_id="abc", content_id="content_456", status=True
        )


def test_when_path_id_is_exactly_5_characters_should_not_raise():
    request = UpdateContentPathStatusRequest(
        path_id="abcde", content_id="content_456", status=True
    )
    assert request.path_id == "abcde"


def test_when_path_id_is_at_maximum_length_should_not_raise():
    max_path_id = "a" * 100
    request = UpdateContentPathStatusRequest(
        path_id=max_path_id, content_id="content_456", status=True
    )
    assert request.path_id == max_path_id


def test_when_path_id_exceeds_100_characters_should_raise():
    long_path_id = "a" * 101
    with pytest.raises(ValueError, match="path_id must not exceed 100 characters"):
        UpdateContentPathStatusRequest(
            path_id=long_path_id, content_id="content_456", status=True
        )


def test_when_content_id_is_empty_should_raise():
    with pytest.raises(ValueError, match="content_id must not be empty"):
        UpdateContentPathStatusRequest(path_id="path_123", content_id="", status=True)


def test_when_content_id_is_too_short_should_raise():
    with pytest.raises(
        ValueError, match="content_id must be at least 5 characters long"
    ):
        UpdateContentPathStatusRequest(
            path_id="path_123", content_id="abc", status=True
        )


def test_when_content_id_is_exactly_5_characters_should_not_raise():
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="abcde", status=True
    )
    assert request.content_id == "abcde"


def test_when_content_id_is_at_maximum_length_should_not_raise():
    max_content_id = "a" * 100
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id=max_content_id, status=True
    )
    assert request.content_id == max_content_id


def test_when_content_id_exceeds_100_characters_should_raise():
    long_content_id = "a" * 101
    with pytest.raises(ValueError, match="content_id must not exceed 100 characters"):
        UpdateContentPathStatusRequest(
            path_id="path_123", content_id=long_content_id, status=True
        )


def test_when_status_is_true_should_accept():
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=True
    )
    assert request.status is True


def test_when_status_is_false_should_accept():
    request = UpdateContentPathStatusRequest(
        path_id="path_123", content_id="content_456", status=False
    )
    assert request.status is False
