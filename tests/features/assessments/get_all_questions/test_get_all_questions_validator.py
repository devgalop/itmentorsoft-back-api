from src.features.assessments.get_all_questions.get_all_questions_request import (
    GetAllQuestionsRequest,
)
import pytest


def test_when_request_is_valid_with_defaults_then_exception_is_not_raised():
    request = GetAllQuestionsRequest()
    assert request.page == 0
    assert request.page_size == 10


def test_when_request_is_valid_with_custom_values_then_exception_is_not_raised():
    request = GetAllQuestionsRequest(page=5, page_size=25)
    assert request.page == 5
    assert request.page_size == 25


def test_when_page_is_negative_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Número de página debe ser un entero no negativo"
    ):
        GetAllQuestionsRequest(page=-1)


def test_when_page_size_is_zero_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetAllQuestionsRequest(page_size=0)


def test_when_page_size_is_negative_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetAllQuestionsRequest(page_size=-5)


def test_when_page_size_exceeds_max_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página no debe exceder 100"):
        GetAllQuestionsRequest(page_size=101)


def test_when_page_size_is_exactly_100_then_exception_is_not_raised():
    request = GetAllQuestionsRequest(page_size=100)
    assert request.page_size == 100


def test_when_page_is_exactly_zero_then_exception_is_not_raised():
    request = GetAllQuestionsRequest(page=0)
    assert request.page == 0
