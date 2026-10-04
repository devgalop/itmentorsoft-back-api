from src.features.reports.get_category_summary.get_category_summary_request import (
    GetCategorySummaryRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetCategorySummaryRequest(category="Mathematics")
    assert request.category == "Mathematics"


def test_when_category_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Categoría no debe estar vacía"):
        GetCategorySummaryRequest(category="")


def test_when_category_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Categoría debe tener al menos 3 caracteres"):
        GetCategorySummaryRequest(category="ab")


def test_when_category_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Categoría no debe exceder 80 caracteres"):
        GetCategorySummaryRequest(category="a" * 81)


def test_when_category_is_exactly_3_characters_then_valid():
    request = GetCategorySummaryRequest(category="abc")
    assert request.category == "abc"


def test_when_category_is_exactly_80_characters_then_valid():
    request = GetCategorySummaryRequest(category="a" * 80)
    assert request.category == "a" * 80


def test_when_category_has_whitespace_then_it_is_stripped():
    request = GetCategorySummaryRequest(category="  Mathematics  ")
    assert request.category == "Mathematics"
