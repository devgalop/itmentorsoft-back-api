from src.features.content_management.register_content.register_content_request import (
    RegisterContentRequest,
)
import pytest


def test_when_request_is_valid_then_exception_is_not_raised():
    request = RegisterContentRequest(
        title="Valid Title Here",
        description="This is a valid description with enough characters",
        url="https://example.com/valid",
        category="novice",
        related_topic=["Python"],
    )
    assert request.title == "Valid Title Here"
    assert request.description == "This is a valid description with enough characters"
    assert request.url == "https://example.com/valid"


def test_when_title_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Título no debe estar vacío"):
        RegisterContentRequest(
            title="",
            description="This is a valid description",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_title_is_too_short_then_exception_is_raised():
    with pytest.raises(ValueError, match="Título debe tener al menos 5 caracteres"):
        RegisterContentRequest(
            title="abcd",
            description="This is a valid description",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_title_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Título no debe exceder 150 caracteres"):
        RegisterContentRequest(
            title="a" * 151,
            description="This is a valid description",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_description_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="Descripción no debe estar vacía"):
        RegisterContentRequest(
            title="Valid Title",
            description="",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_description_is_too_short_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Descripción debe tener al menos 10 caracteres"
    ):
        RegisterContentRequest(
            title="Valid Title",
            description="Short",
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_description_is_too_long_then_exception_is_raised():
    with pytest.raises(ValueError, match="Descripción no debe exceder 300 caracteres"):
        RegisterContentRequest(
            title="Valid Title",
            description="a" * 301,
            url="https://example.com/test",
            category="novice",
            related_topic=[],
        )


def test_when_url_is_missing_then_exception_is_raised():
    with pytest.raises(ValueError, match="URL no debe estar vacía"):
        RegisterContentRequest(
            title="Valid Title",
            description="This is a valid description",
            url="",
            category="novice",
            related_topic=[],
        )


def test_when_url_is_invalid_format_then_exception_is_raised():
    with pytest.raises(
        ValueError, match="Formato de URL inválido, debe comenzar con https://"
    ):
        RegisterContentRequest(
            title="Valid Title",
            description="This is a valid description",
            url="http://example.com/test",
            category="novice",
            related_topic=[],
        )
