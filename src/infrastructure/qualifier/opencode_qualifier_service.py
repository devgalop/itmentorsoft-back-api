import asyncio
import json
import logging
import uuid

from openai import OpenAI

from itmentorsoft_persistence.dto import QualifierResult
from src.features.assessments.shared.qualifier_service import (
    BatchQualificationError,
    BatchQualifierPrompt,
    QualifierService,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants

logger = logging.getLogger(__name__)


class OpencodeQualifierService(QualifierService):
    """Qualifier service implementation using the OpenAI-compatible Opencode API."""

    def __init__(self, model_id: str):
        self.model_id = model_id
        self.client = OpenAI(
            api_key=EnvironmentVariablesConstants.OPENCODE_API_KEY,
            base_url=EnvironmentVariablesConstants.OPENCODE_API_URL,
        )

    async def qualify(self, qualifier_prompt):
        """Single-answer qualification (not implemented for batch-only service)."""
        raise NotImplementedError(
            "OpencodeQualifierService only supports batch qualification. "
            "Use qualify_batch instead."
        )

    async def qualify_batch(
        self, batch_prompt: BatchQualifierPrompt
    ) -> list[QualifierResult]:
        """Evaluate multiple answers in a single LLM call.

        Sends all rubrics and answers to the LLM in one request, parses the
        JSON array response, and returns QualifierResult objects in the same
        order as the input answers.

        Raises:
            ValueError: If the LLM returns an empty/None response.
            BatchQualificationError: If the response cannot be parsed as a
                valid JSON array.
        """
        # Build lookup maps for answer -> question matching
        answer_to_question = {
            answer.answer_id: rubric
            for answer, rubric in zip(batch_prompt.answers, batch_prompt.rubrics)
        }
        expected_answer_ids = {answer.answer_id for answer in batch_prompt.answers}

        # Build the prompt content
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(batch_prompt)

        # Call the LLM
        response = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        raw_content = response.choices[0].message.content

        # Validate non-empty response
        if not raw_content:
            raise ValueError("LLM returned empty response")

        # Parse JSON
        try:
            parsed = json.loads(raw_content)
        except json.JSONDecodeError:
            raise BatchQualificationError(
                raw_response=raw_content,
                message="Failed to parse batch qualification response as JSON",
            )

        # Must be a list
        if not isinstance(parsed, list):
            raise BatchQualificationError(
                raw_response=raw_content,
                message="Batch qualification response is not a JSON array",
            )

        # Map LLM results by answer_id for lookup
        results_by_answer_id = {}
        for item in parsed:
            answer_id = item.get("answer_id")
            if answer_id in expected_answer_ids:
                results_by_answer_id[answer_id] = item
            else:
                logger.warning(
                    "LLM returned result for unknown answer_id '%s', discarding",
                    answer_id,
                )

        # Build QualifierResult list in input order
        results = []
        for answer in batch_prompt.answers:
            item = results_by_answer_id.get(answer.answer_id)
            if item is None:
                continue

            rubric = answer_to_question[answer.answer_id]
            qualifier_result = QualifierResult(
                id=str(uuid.uuid4()),
                question_id=rubric.question_id,
                user_id=batch_prompt.user_id,
                score=item["score"],
                feedback=item["feedback"],
                key_concepts_detected=item.get("key_concepts_detected", []),
                misconceptions_detected=item.get("misconceptions_detected", []),
                question_topic=rubric.concept,
                assessment_id=batch_prompt.assessment_id,
                question_difficulty=rubric.difficulty.value,
                answer_id=answer.answer_id,
            )
            results.append(qualifier_result)

        return results

    def _build_system_prompt(self) -> str:
        return (
            "You are an expert educational assessor. You will receive a batch of "
            "questions with their rubrics and student answers. Evaluate each answer "
            "and return a JSON array with one object per answer. Each object must "
            "contain: answer_id (string), score (integer 0-100), feedback (string), "
            "key_concepts_detected (array of strings), misconceptions_detected "
            "(array of strings). Return ONLY the JSON array, no other text."
        )

    def _build_user_prompt(self, batch_prompt: BatchQualifierPrompt) -> str:
        rubrics_data = []
        for rubric in batch_prompt.rubrics:
            rubrics_data.append(
                {
                    "question_id": rubric.question_id,
                    "text": rubric.text_to_evaluate,
                    "concept": rubric.concept,
                    "definition": rubric.definition,
                    "correct_sample": rubric.correct_sample,
                    "wrong_sample": rubric.wrong_sample,
                    "rubric_scores": [
                        {"score": r.score, "explanation": r.explanation}
                        for r in rubric.rubric
                    ],
                }
            )

        answers_data = []
        for answer in batch_prompt.answers:
            answers_data.append(
                {
                    "answer_id": answer.answer_id,
                    "question_id": answer.question_id,
                    "answer_text": answer.answer,
                }
            )

        return json.dumps(
            {
                "qualifier_mode": batch_prompt.qualifier_mode,
                "rubrics": rubrics_data,
                "answers": answers_data,
            },
            ensure_ascii=False,
        )
