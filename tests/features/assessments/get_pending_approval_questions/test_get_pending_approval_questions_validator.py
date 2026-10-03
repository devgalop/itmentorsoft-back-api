from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_request import (
    GetPendingApprovalQuestionsRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetPendingApprovalQuestionsRequest(page=0, page_size=10)
    assert request.page == 0
    assert request.page_size == 10


def test_when_request_uses_defaults_then_values_are_correct():
    request = GetPendingApprovalQuestionsRequest()
    assert request.page == 0
    assert request.page_size == 10


def test_when_page_is_negative_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Número de página debe ser un entero no negativo"
    ):
        GetPendingApprovalQuestionsRequest(page=-1, page_size=10)


def test_when_page_size_is_zero_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetPendingApprovalQuestionsRequest(page=0, page_size=0)


def test_when_page_size_is_negative_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página debe ser al menos 1"):
        GetPendingApprovalQuestionsRequest(page=0, page_size=-5)


def test_when_page_size_exceeds_maximum_then_exception_is_raised():
    with pytest.raises(ValueError, match="Tamaño de página no debe exceder 100"):
        GetPendingApprovalQuestionsRequest(page=0, page_size=101)


def test_when_page_size_is_at_minimum_boundary_then_exception_is_not_raised():
    request = GetPendingApprovalQuestionsRequest(page=0, page_size=1)
    assert request.page_size == 1


def test_when_page_size_is_at_maximum_boundary_then_exception_is_not_raised():
    request = GetPendingApprovalQuestionsRequest(page=0, page_size=100)
    assert request.page_size == 100


def test_when_page_is_zero_then_exception_is_not_raised():
    request = GetPendingApprovalQuestionsRequest(page=0, page_size=10)
    assert request.page == 0


def test_when_page_is_large_then_exception_is_not_raised():
    request = GetPendingApprovalQuestionsRequest(page=999, page_size=10)
    assert request.page == 999


def test_when_page_and_page_size_are_custom_then_values_are_correct():
    request = GetPendingApprovalQuestionsRequest(page=5, page_size=25)
    assert request.page == 5
    assert request.page_size == 25
