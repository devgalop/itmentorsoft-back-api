from src.features.assessments.get_questions_by_category.get_questions_by_category_request import (
    GetQuestionsByCategoryRequest,
)
import pytest

from src.features.assessments.shared.question_categories import QUESTION_CATEGORIES


def test_when_request_is_valid_then_exception_is_not_raised():
    request = GetQuestionsByCategoryRequest(category=QUESTION_CATEGORIES[0])
    assert request.category == QUESTION_CATEGORIES[0]


def test_when_category_is_empty_then_exception_is_raised():
    with pytest.raises(ValueError, match="Category cannot be empty"):
        GetQuestionsByCategoryRequest(category="")


def test_when_category_is_invalid_then_exception_is_raised():
    with pytest.raises(ValueError, match="Invalid category"):
        GetQuestionsByCategoryRequest(category="invalid_category")


def test_when_category_is_diseno_orientado_a_objetos_then_exception_is_not_raised():
    request = GetQuestionsByCategoryRequest(category="Diseño orientado a objetos")
    assert request.category == "Diseño orientado a objetos"


def test_when_category_is_api_y_sistemas_distribuidos_then_exception_is_not_raised():
    request = GetQuestionsByCategoryRequest(category="APIs y sistemas distribuidos")
    assert request.category == "APIs y sistemas distribuidos"
