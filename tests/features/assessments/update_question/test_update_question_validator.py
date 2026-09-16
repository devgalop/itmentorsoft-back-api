from src.features.assessments.update_question.update_question_request import (
    UpdateQuestionRequest,
)
import pytest

VALID_UPDATE_REQUEST = dict(
    text="Updated text explaining polymorphism in OOP with clear examples",
    concept="Object Oriented Programming",
    definition="OOP is a programming paradigm based on objects and classes with updated definition",
    simple_explanation="OOP groups data and behavior together into reusable updated objects",
    correct_sample="Polymorphism allows objects of different types to be treated as instances of the same type",
    wrong_sample="Polymorphism means having many forms but it is not related to OOP at all",
    common_misconception=[
        "Polymorphism and inheritance are the exact same thing in OOP",
        "Polymorphism only works with interfaces and not with abstract classes",
    ],
    rubric=[
        {"score": 3, "criteria": "Complete and correct answer with clear examples"}
    ],
    semantic_keywords=["OOP", "polymorphism"],
    difficulty="intermedio",
    topic="Polymorphism",
)


def test_when_request_is_valid_then_exception_is_not_raised():
    request = UpdateQuestionRequest(**VALID_UPDATE_REQUEST)
    assert request.text == VALID_UPDATE_REQUEST["text"]
    assert request.concept == VALID_UPDATE_REQUEST["concept"]


def test_when_text_is_empty_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "text": ""}
    with pytest.raises(ValueError, match="Text cannot be empty"):
        UpdateQuestionRequest(**data)


def test_when_text_is_too_short_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "text": "short"}
    with pytest.raises(ValueError, match="Text must be at least 20 characters long"):
        UpdateQuestionRequest(**data)


def test_when_concept_is_empty_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "concept": ""}
    with pytest.raises(ValueError, match="Concept cannot be empty"):
        UpdateQuestionRequest(**data)


def test_when_definition_is_empty_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "definition": ""}
    with pytest.raises(ValueError, match="Definition cannot be empty"):
        UpdateQuestionRequest(**data)


def test_when_simple_explanation_is_too_short_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "simple_explanation": "short"}
    with pytest.raises(
        ValueError, match="Simple explanation must be at least 20 characters long"
    ):
        UpdateQuestionRequest(**data)


def test_when_correct_sample_is_too_long_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "correct_sample": "a" * 301}
    with pytest.raises(
        ValueError, match="Correct sample cannot be longer than 300 characters"
    ):
        UpdateQuestionRequest(**data)


def test_when_wrong_sample_is_empty_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "wrong_sample": ""}
    with pytest.raises(ValueError, match="Wrong sample cannot be empty"):
        UpdateQuestionRequest(**data)


def test_when_common_misconception_has_less_than_2_items_then_exception_is_raised():
    data = {
        **VALID_UPDATE_REQUEST,
        "common_misconception": ["Only one item here for test"],
    }
    with pytest.raises(
        ValueError, match="Common misconception must have at least 2 items"
    ):
        UpdateQuestionRequest(**data)


def test_when_rubric_score_is_out_of_range_then_exception_is_raised():
    data = {
        **VALID_UPDATE_REQUEST,
        "rubric": [{"score": 5, "criteria": "This is a valid criteria text here"}],
    }
    with pytest.raises(ValueError, match="Score must be between 0 and 3"):
        UpdateQuestionRequest(**data)


def test_when_rubric_criteria_is_too_short_then_exception_is_raised():
    data = {
        **VALID_UPDATE_REQUEST,
        "rubric": [{"score": 1, "criteria": "Short"}],
    }
    with pytest.raises(
        ValueError, match="Criteria must be at least 10 characters long"
    ):
        UpdateQuestionRequest(**data)


def test_when_semantic_keywords_is_empty_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "semantic_keywords": []}
    with pytest.raises(ValueError, match="Semantic keywords cannot be empty"):
        UpdateQuestionRequest(**data)


def test_when_semantic_keyword_is_too_short_then_exception_is_raised():
    data = {**VALID_UPDATE_REQUEST, "semantic_keywords": ["a"]}
    with pytest.raises(
        ValueError, match="Each semantic keyword must be at least 2 characters long"
    ):
        UpdateQuestionRequest(**data)
