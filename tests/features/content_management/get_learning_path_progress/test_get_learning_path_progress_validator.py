import pytest

from src.features.content_management.get_learning_path_progress.get_learning_path_progress_request import (
    GetLearningPathProgressRequest,
)


def test_when_path_id_is_valid_should_not_raise():
    request = GetLearningPathProgressRequest(path_id="path_123")
    assert request.path_id == "path_123"


def test_when_path_id_is_empty_should_raise():
    with pytest.raises(ValueError, match="path_id is required."):
        GetLearningPathProgressRequest(path_id="")


def test_when_path_id_is_too_short_should_raise():
    with pytest.raises(ValueError, match="path_id must be at least 5 characters long."):
        GetLearningPathProgressRequest(path_id="abc")


def test_when_path_id_is_exactly_5_characters_should_not_raise():
    request = GetLearningPathProgressRequest(path_id="abcde")
    assert request.path_id == "abcde"


def test_when_path_id_is_at_maximum_length_should_not_raise():
    max_path_id = "a" * 100
    request = GetLearningPathProgressRequest(path_id=max_path_id)
    assert request.path_id == max_path_id


def test_when_path_id_exceeds_100_characters_should_raise():
    long_path_id = "a" * 101
    with pytest.raises(ValueError, match="path_id must not exceed 100 characters."):
        GetLearningPathProgressRequest(path_id=long_path_id)
