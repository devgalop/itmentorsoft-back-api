import pytest
from pydantic import ValidationError

from src.features.content_management.update_resource_content.update_resource_content_request import (
    UpdateResourceContentRequest,
)

VALID_TITLE = "Python Programming Basics"
VALID_DESCRIPTION = (
    "A comprehensive guide covering Python fundamentals and best practices"
)
VALID_URL = "https://example.com/python-basics"
VALID_CATEGORY = "novice"


def make_valid_request(**overrides) -> UpdateResourceContentRequest:
    defaults = {
        "title": VALID_TITLE,
        "description": VALID_DESCRIPTION,
        "url": VALID_URL,
        "category": VALID_CATEGORY,
        "related_topic": [],
    }
    return UpdateResourceContentRequest(**{**defaults, **overrides})


# --- Title validation ---


def test_when_title_is_valid_then_exception_is_not_raised():
    req = make_valid_request()
    assert req.title == VALID_TITLE


def test_when_title_is_too_short_then_raises_validation_error():
    with pytest.raises(
        ValidationError, match="Título debe tener al menos 5 caracteres"
    ):
        make_valid_request(title="Py")


def test_when_title_is_too_long_then_raises_validation_error():
    with pytest.raises(ValidationError, match="Título no debe exceder 150 caracteres"):
        make_valid_request(title="a" * 151)


def test_when_title_is_empty_then_raises_validation_error():
    with pytest.raises(ValidationError, match="Título no debe estar vacío"):
        make_valid_request(title="")


def test_when_title_is_exactly_5_chars_then_exception_is_not_raised():
    req = make_valid_request(title="Hello")
    assert req.title == "Hello"


def test_when_title_is_exactly_150_chars_then_exception_is_not_raised():
    req = make_valid_request(title="a" * 150)
    assert len(req.title) == 150


# --- Description validation ---


def test_when_description_is_valid_then_exception_is_not_raised():
    req = make_valid_request()
    assert req.description == VALID_DESCRIPTION


def test_when_description_is_too_short_then_raises_validation_error():
    with pytest.raises(
        ValidationError, match="Descripción debe tener al menos 10 caracteres"
    ):
        make_valid_request(description="Short")


def test_when_description_is_too_long_then_raises_validation_error():
    with pytest.raises(
        ValidationError, match="Descripción no debe exceder 300 caracteres"
    ):
        make_valid_request(description="a" * 301)


def test_when_description_is_empty_then_raises_validation_error():
    with pytest.raises(ValidationError, match="Descripción no debe estar vacía"):
        make_valid_request(description="")


def test_when_description_is_exactly_10_chars_then_exception_is_not_raised():
    req = make_valid_request(description="1234567890")
    assert len(req.description) == 10


def test_when_description_is_exactly_300_chars_then_exception_is_not_raised():
    req = make_valid_request(description="a" * 300)
    assert len(req.description) == 300


# --- URL validation ---


def test_when_url_is_valid_then_exception_is_not_raised():
    req = make_valid_request()
    assert req.url == VALID_URL


def test_when_url_is_empty_then_raises_validation_error():
    with pytest.raises(ValidationError, match="URL no debe estar vacía"):
        make_valid_request(url="")


def test_when_url_does_not_start_with_https_then_raises_validation_error():
    with pytest.raises(
        ValidationError, match="Formato de URL inválido, debe comenzar con https://"
    ):
        make_valid_request(url="http://example.com")


def test_when_url_starts_with_https_then_exception_is_not_raised():
    req = make_valid_request(url="https://docs.python.org/3/tutorial/")
    assert req.url == "https://docs.python.org/3/tutorial/"


# --- Related topic and category ---


def test_when_related_topic_is_empty_list_then_exception_is_not_raised():
    req = make_valid_request(related_topic=[])
    assert req.related_topic == []


def test_when_related_topic_has_values_then_exception_is_not_raised():
    req = make_valid_request(related_topic=["Python", "OOP"])
    assert req.related_topic == ["Python", "OOP"]


def test_when_category_is_valid_then_exception_is_not_raised():
    req = make_valid_request(category="emerging")
    assert req.category == "emerging"


def test_when_category_is_empty_string_then_exception_is_not_raised():
    req = make_valid_request(category="")
    assert req.category == ""
