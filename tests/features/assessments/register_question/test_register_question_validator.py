from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
import pytest

VALID_REGISTER_REQUEST = dict(
    text="Explain the difference between abstraction and encapsulation in OOP",
    concept="Object Oriented Programming",
    definition="OOP is a programming paradigm based on objects and classes",
    simple_explanation="OOP groups data and behavior together into reusable objects",
    correct_sample="Abstraction hides implementation details while encapsulation bundles data",
    wrong_sample="They are the same thing, both hide data from the user completely",
    common_misconception=[
        "Abstraction and encapsulation are the same concept in OOP",
        "Encapsulation only refers to using private fields inside a class",
    ],
    rubric=[{"score": 3, "criteria": "Complete and correct answer with examples"}],
    semantic_keywords=["OOP", "abstraction"],
    difficulty="intermedio",
    topic="Object Oriented Programming",
)


def test_when_request_is_valid_then_exception_is_not_raised():
    request = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    assert request.text == VALID_REGISTER_REQUEST["text"]
    assert request.concept == VALID_REGISTER_REQUEST["concept"]
    assert len(request.common_misconception) == 2
    assert len(request.semantic_keywords) == 2


def test_when_text_is_empty_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "text": ""}
    with pytest.raises(ValueError, match="Text cannot be empty"):
        RegisterQuestionRequest(**data)


def test_when_text_is_too_short_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "text": "short"}
    with pytest.raises(ValueError, match="Text must be at least 20 characters long"):
        RegisterQuestionRequest(**data)


def test_when_text_is_too_long_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "text": "a" * 501}
    with pytest.raises(ValueError, match="Text cannot be longer than 500 characters"):
        RegisterQuestionRequest(**data)


def test_when_concept_is_empty_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "concept": ""}
    with pytest.raises(ValueError, match="Concept cannot be empty"):
        RegisterQuestionRequest(**data)


def test_when_concept_is_too_short_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "concept": "short"}
    with pytest.raises(ValueError, match="Concept must be at least 10 characters long"):
        RegisterQuestionRequest(**data)


def test_when_concept_is_too_long_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "concept": "a" * 151}
    with pytest.raises(
        ValueError, match="Concept cannot be longer than 150 characters"
    ):
        RegisterQuestionRequest(**data)


def test_when_definition_is_empty_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "definition": ""}
    with pytest.raises(ValueError, match="Definition cannot be empty"):
        RegisterQuestionRequest(**data)


def test_when_definition_is_too_short_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "definition": "short"}
    with pytest.raises(
        ValueError, match="Definition must be at least 20 characters long"
    ):
        RegisterQuestionRequest(**data)


def test_when_definition_is_too_long_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "definition": "a" * 501}
    with pytest.raises(
        ValueError, match="Definition cannot be longer than 500 characters"
    ):
        RegisterQuestionRequest(**data)


def test_when_common_misconception_has_less_than_2_items_then_exception_is_raised():
    data = {
        **VALID_REGISTER_REQUEST,
        "common_misconception": ["Only one item here for test"],
    }
    with pytest.raises(
        ValueError, match="Common misconception must have at least 2 items"
    ):
        RegisterQuestionRequest(**data)


def test_when_common_misconception_is_empty_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "common_misconception": []}
    with pytest.raises(ValueError, match="Common misconception cannot be empty"):
        RegisterQuestionRequest(**data)


def test_when_rubric_score_is_out_of_range_then_exception_is_raised():
    data = {
        **VALID_REGISTER_REQUEST,
        "rubric": [{"score": 5, "criteria": "This is a valid criteria text"}],
    }
    with pytest.raises(ValueError, match="Score must be between 0 and 3"):
        RegisterQuestionRequest(**data)


def test_when_rubric_criteria_is_too_short_then_exception_is_raised():
    data = {
        **VALID_REGISTER_REQUEST,
        "rubric": [{"score": 1, "criteria": "Short"}],
    }
    with pytest.raises(
        ValueError, match="Criteria must be at least 10 characters long"
    ):
        RegisterQuestionRequest(**data)


def test_when_semantic_keywords_is_empty_then_exception_is_raised():
    data = {**VALID_REGISTER_REQUEST, "semantic_keywords": []}
    with pytest.raises(ValueError, match="Semantic keywords cannot be empty"):
        RegisterQuestionRequest(**data)
