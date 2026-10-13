import pytest

from src.features.content_management.get_complete_learning_path.get_complete_learning_path_request import (
    GetCompleteLearningPathRequest,
)


def test_when_user_id_is_valid_should_not_raise():
    request = GetCompleteLearningPathRequest(user_id="user_123")
    assert request.user_id == "user_123"


def test_when_user_id_is_empty_should_raise():
    with pytest.raises(ValueError, match="User ID must not be empty"):
        GetCompleteLearningPathRequest(user_id="")


def test_when_user_id_is_too_short_should_raise():
    with pytest.raises(ValueError, match="User ID must be at least 5 characters"):
        GetCompleteLearningPathRequest(user_id="abc")


def test_when_user_id_is_exactly_5_characters_should_not_raise():
    request = GetCompleteLearningPathRequest(user_id="abcde")
    assert request.user_id == "abcde"


def test_when_user_id_is_at_maximum_length_should_not_raise():
    max_user_id = "a" * 100
    request = GetCompleteLearningPathRequest(user_id=max_user_id)
    assert request.user_id == max_user_id


def test_when_user_id_exceeds_100_characters_should_raise():
    long_user_id = "a" * 101
    with pytest.raises(ValueError, match="User ID must not exceed 100 characters"):
        GetCompleteLearningPathRequest(user_id=long_user_id)


def test_when_page_is_zero_should_not_raise():
    request = GetCompleteLearningPathRequest(user_id="user_123", page=0)
    assert request.page == 0


def test_when_page_is_positive_should_not_raise():
    request = GetCompleteLearningPathRequest(user_id="user_123", page=5)
    assert request.page == 5


def test_when_page_is_negative_should_raise():
    with pytest.raises(ValueError, match="Must be non-negative"):
        GetCompleteLearningPathRequest(user_id="user_123", page=-1)


def test_when_page_size_is_zero_should_not_raise():
    request = GetCompleteLearningPathRequest(user_id="user_123", page_size=0)
    assert request.page_size == 0


def test_when_page_size_is_positive_should_not_raise():
    request = GetCompleteLearningPathRequest(user_id="user_123", page_size=20)
    assert request.page_size == 20


def test_when_page_size_is_negative_should_raise():
    with pytest.raises(ValueError, match="Must be non-negative"):
        GetCompleteLearningPathRequest(user_id="user_123", page_size=-1)


def test_default_page_and_page_size():
    request = GetCompleteLearningPathRequest(user_id="user_123")
    assert request.page == 0
    assert request.page_size == 10


def test_all_fields_valid():
    request = GetCompleteLearningPathRequest(user_id="user_123", page=2, page_size=15)
    assert request.user_id == "user_123"
    assert request.page == 2
    assert request.page_size == 15
