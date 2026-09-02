import json
from pathlib import Path
import uuid

import aiofiles
from sqlalchemy import select

from src.features.assessments.shared.question import (
    Question,
    QuestionBuilder,
    QuestionDifficulty,
    QuestionRubricScore,
    QuestionStatus,
)
from itmentorsoft_persistence.models import (
    QuestionEntity,
    QuestionRubricScoreEntity,
)
from itmentorsoft_persistence import AsyncSessionLocal

_PROJECT_ROOT = Path(__file__).resolve().parents[4]
_QUESTIONS_FILE = _PROJECT_ROOT / "docs" / "resources" / "sample_questions.json"


def _parse_rubric(raw: dict[str, str]) -> list[QuestionRubricScore]:
    """Convert a raw rubric dict (str score -> explanation) to domain objects."""
    return [
        QuestionRubricScore(score=int(score_key), explanation=explanation)
        for score_key, explanation in raw.items()
    ]


async def read_questions_from_file(file_path: str) -> list[Question]:
    """Read JSON file asynchronously and map each entry to a Question domain object."""
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
        content = await f.read()

    raw_items = json.loads(content)
    questions: list[Question] = []

    for item in raw_items:
        rubric_scores = _parse_rubric(item.get("criterios_rubrica", {}))

        builder = (
            QuestionBuilder()
            .set_question_id(item["pregunta_id"])
            .set_text_to_evaluate(item.get("texto_a_evaluar", item.get("text", "")))
            .set_concept(item["concepto"])
            .set_definition(item["definicion"])
            .set_simple_explanation(item["explicacion_simple"])
            .set_correct_sample(item["ejemplo_correcto"])
            .set_wrong_sample(item["ejemplo_incorrecto"])
            .add_common_misconceptions(item.get("errores_comunes", []))
            .add_semantic_keywords(item.get("keywords_semanticas", []))
            .add_rubrics(rubric_scores)
            .set_difficulty(
                QuestionDifficulty(
                    item.get("dificultad", QuestionDifficulty.EASY.value)
                )
            )
            .set_status(QuestionStatus.PUBLISHED)
            .set_classification(item.get("categoria_contenido", ""))
            .set_version(1)
        )

        questions.append(builder.build())

    return questions


def map_question_to_entity(question: Question) -> QuestionEntity:
    """Pure function: map a domain Question to a QuestionEntity with nested rubric entities."""
    question_id = uuid.uuid4().hex
    entity = QuestionEntity(
        id=question_id,
        text=question.text_to_evaluate,
        concept=question.concept,
        definition=question.definition,
        simple_explanation=question.simple_explanation,
        correct_sample=question.correct_sample,
        wrong_sample=question.wrong_sample,
        common_misconceptions="|".join(question.common_misconception),
        semantic_keywords="|".join(question.semantic_keywords),
        status=question.status.value,
        difficulty=question.difficulty.value,
        classification=question.classification,
        version=question.version,
    )

    entity.rubric = [
        QuestionRubricScoreEntity(
            question_id=question_id,
            score=rubric.score,
            explanation=rubric.explanation,
        )
        for rubric in question.rubric
    ]

    return entity


async def seed_questions() -> None:
    async with AsyncSessionLocal() as session:
        smt = await session.execute(select(QuestionEntity))
        existing = smt.scalars().first()

        if existing:
            print("questions already seeded. Skipping seeding.")
            return

        questions = await read_questions_from_file(str(_QUESTIONS_FILE))

        for question in questions:
            entity = map_question_to_entity(question)
            session.add(entity)

        await session.commit()
        print("questions seeded.")
