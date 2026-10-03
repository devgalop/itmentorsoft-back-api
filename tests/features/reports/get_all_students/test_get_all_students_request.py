from src.features.reports.get_all_students.get_all_students_request import (
    GetAllStudentsRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetAllStudentsRequest(page=0, page_size=10)
    assert request.page == 0
    assert request.page_size == 10


def test_when_page_is_negative_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Número de página debe ser un entero no negativo"
    ):
        GetAllStudentsRequest(page=-1, page_size=10)


def test_when_page_size_is_zero_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetAllStudentsRequest(page=0, page_size=0)


def test_when_page_size_is_negative_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetAllStudentsRequest(page=0, page_size=-5)


def test_when_page_size_exceeds_100_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página no debe exceder 100"):
        GetAllStudentsRequest(page=0, page_size=101)


def test_when_page_is_zero_then_valid():
    request = GetAllStudentsRequest(page=0, page_size=10)
    assert request.page == 0


def test_when_page_size_is_one_then_valid():
    request = GetAllStudentsRequest(page=1, page_size=1)
    assert request.page_size == 1


def test_when_page_size_is_exactly_100_then_valid():
    request = GetAllStudentsRequest(page=0, page_size=100)
    assert request.page_size == 100


def test_when_defaults_are_used_then_valid():
    request = GetAllStudentsRequest()
    assert request.page == 0
    assert request.page_size == 10
