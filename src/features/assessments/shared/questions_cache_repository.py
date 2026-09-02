from time import time

from itmentorsoft_persistence.repositories import (
    QuestionAssessmentRepository,
)
from itmentorsoft_persistence.dto import (
    EvaluativeQuestion,
    QuestionDifficulty,
)


class EvaluativeQuestionsCache:
    def __init__(self, questions: list[EvaluativeQuestion], expiration_time: int):
        self.questions = questions
        self.expiration_time = expiration_time


class QuestionsCacheRepository(QuestionAssessmentRepository):

    _shared_cache: dict[str, EvaluativeQuestionsCache] = {}
    _cache_expiration_time_seconds = 3600

    def __init__(self, assessment_repository: QuestionAssessmentRepository):
        self.assessment_repository = assessment_repository

    async def get_question_by_level(
        self, difficulty: QuestionDifficulty
    ) -> list[EvaluativeQuestion]:
        if self.should_refresh_cache(difficulty.name):
            questions = await self.assessment_repository.get_question_by_level(
                difficulty
            )
            expiration_time = int(time()) + self._cache_expiration_time_seconds
            self._shared_cache[difficulty.name] = EvaluativeQuestionsCache(
                questions, expiration_time
            )

        return self._shared_cache[difficulty.name].questions

    async def get_questions_by_category(
        self, category: str
    ) -> list[EvaluativeQuestion]:
        if self.should_refresh_cache(category):
            questions = await self.assessment_repository.get_questions_by_category(
                category
            )
            expiration_time = int(time()) + self._cache_expiration_time_seconds
            self._shared_cache[category] = EvaluativeQuestionsCache(
                questions, expiration_time
            )

        return self._shared_cache[category].questions

    async def get_questions_by_topic(
        self, topic: str, difficulty: QuestionDifficulty
    ) -> list[EvaluativeQuestion]:
        cache_key = f"{topic}_{difficulty.name}"
        if self.should_refresh_cache(cache_key):
            questions = await self.assessment_repository.get_questions_by_topic(
                topic, difficulty
            )
            expiration_time = int(time()) + self._cache_expiration_time_seconds
            self._shared_cache[cache_key] = EvaluativeQuestionsCache(
                questions, expiration_time
            )

        return self._shared_cache[cache_key].questions

    def should_refresh_cache(self, key: str) -> bool:
        """Validate if the cache should be refreshed for a given key.

        Args:
            key (str): The key to check in the cache.

        Returns:
            bool: True if the cache should be refreshed, False otherwise.
        """
        self._purge_expired()
        return (
            not self._shared_cache
            or key not in self._shared_cache
            or self._shared_cache[key].expiration_time < int(time())
        )

    def _purge_expired(self) -> None:
        """Remove expired elements from cache"""
        now = int(time())
        expired_keys = [
            k for k, v in self._shared_cache.items() if now > v.expiration_time
        ]
        for key in expired_keys:
            del self._shared_cache[key]
