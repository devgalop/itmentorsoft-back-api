from src.features.content_management.get_all_contents.get_all_contents_request import (
    GetAllContentsRequest,
)
import pytest


def test_when_request_uses_default_values_then_exception_is_not_raised():
    request = GetAllContentsRequest()
    assert request.page == 0
    assert request.page_size == 10


def test_when_request_has_valid_custom_values_then_exception_is_not_raised():
    request = GetAllContentsRequest(page=2, page_size=50)
    assert request.page == 2
    assert request.page_size == 50


def test_when_page_is_zero_then_exception_is_not_raised():
    request = GetAllContentsRequest(page=0)
    assert request.page == 0


def test_when_page_is_negative_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Número de página debe ser un entero no negativo"
    ):
        GetAllContentsRequest(page=-1)


def test_when_page_size_is_one_then_exception_is_not_raised():
    request = GetAllContentsRequest(page_size=1)
    assert request.page_size == 1


def test_when_page_size_is_zero_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetAllContentsRequest(page_size=0)


def test_when_page_size_is_negative_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetAllContentsRequest(page_size=-5)


def test_when_page_size_is_100_then_exception_is_not_raised():
    request = GetAllContentsRequest(page_size=100)
    assert request.page_size == 100


def test_when_page_size_exceeds_100_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página no debe exceder 100"):
        GetAllContentsRequest(page_size=101)
