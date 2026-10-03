from src.features.reports.get_all_students_by_category.get_all_students_by_category_request import (
    GetStudentsByCategoryRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetStudentsByCategoryRequest(category="Mathematics", page=0, page_size=10)
    assert request.category == "Mathematics"
    assert request.page == 0
    assert request.page_size == 10


def test_when_category_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Categoría no debe estar vacía"):
        GetStudentsByCategoryRequest(category="", page=0, page_size=10)


def test_when_category_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Categoría debe tener al menos 3 caracteres"):
        GetStudentsByCategoryRequest(category="ab", page=0, page_size=10)


def test_when_category_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Categoría no debe exceder 80 caracteres"):
        GetStudentsByCategoryRequest(category="a" * 81, page=0, page_size=10)


def test_when_page_is_negative_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Número de página debe ser un entero no negativo"
    ):
        GetStudentsByCategoryRequest(category="Mathematics", page=-1, page_size=10)


def test_when_page_size_is_zero_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetStudentsByCategoryRequest(category="Mathematics", page=0, page_size=0)


def test_when_page_size_exceeds_100_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página no debe exceder 100"):
        GetStudentsByCategoryRequest(category="Mathematics", page=0, page_size=101)


def test_when_category_is_exactly_3_characters_then_valid():
    request = GetStudentsByCategoryRequest(category="abc", page=0, page_size=10)
    assert request.category == "abc"


def test_when_category_is_exactly_80_characters_then_valid():
    request = GetStudentsByCategoryRequest(category="a" * 80, page=0, page_size=10)
    assert request.category == "a" * 80


def test_when_page_is_zero_then_valid():
    request = GetStudentsByCategoryRequest(category="Mathematics", page=0, page_size=10)
    assert request.page == 0


def test_when_page_size_is_one_then_valid():
    request = GetStudentsByCategoryRequest(category="Mathematics", page=0, page_size=1)
    assert request.page_size == 1


def test_when_page_size_is_exactly_100_then_valid():
    request = GetStudentsByCategoryRequest(
        category="Mathematics", page=0, page_size=100
    )
    assert request.page_size == 100
