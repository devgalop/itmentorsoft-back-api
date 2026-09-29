import pytest

from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_request import (
    GetAllQuestionsByVersionsRequest,
)


def test_valid_defaults():
    request = GetAllQuestionsByVersionsRequest()
    assert request.page == 0
    assert request.page_size == 10


def test_valid_custom_values():
    request = GetAllQuestionsByVersionsRequest(page=5, page_size=50)
    assert request.page == 5
    assert request.page_size == 50


def test_valid_page_zero():
    request = GetAllQuestionsByVersionsRequest(page=0)
    assert request.page == 0


def test_valid_page_size_min():
    request = GetAllQuestionsByVersionsRequest(page_size=1)
    assert request.page_size == 1


def test_valid_page_size_max():
    request = GetAllQuestionsByVersionsRequest(page_size=100)
    assert request.page_size == 100


def test_negative_page_raises_error():
    with pytest.raises(ValueError, match="Page must be a non-negative integer"):
        GetAllQuestionsByVersionsRequest(page=-1)


def test_page_size_zero_raises_error():
    with pytest.raises(ValueError, match="Page size must be at least 1"):
        GetAllQuestionsByVersionsRequest(page_size=0)


def test_page_size_negative_raises_error():
    with pytest.raises(ValueError, match="Page size must be at least 1"):
        GetAllQuestionsByVersionsRequest(page_size=-5)


def test_page_size_exceeds_max_raises_error():
    with pytest.raises(ValueError, match="Page size must not exceed 100"):
        GetAllQuestionsByVersionsRequest(page_size=101)
