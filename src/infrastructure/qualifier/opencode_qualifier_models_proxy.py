from time import time

from src.features.assessments.shared.qualifier_service import QualifierModelsService
from src.infrastructure.qualifier.opencode_qualifier_service import (
    OpencodeQualifierService,
)


class ModelsResponse:
    def __init__(self, models: list[str], expiration_time: int):
        self.models = models
        self.expiration_time = expiration_time


class OpencodeQualifierModelsProxy(QualifierModelsService):

    def __init__(self):
        self.qualifier_service = OpencodeQualifierService()
        self._cache_expiration_time_seconds = 14400  # 4 hours
        self._shared_cache: dict[str, ModelsResponse] = {}

    async def get_available_models(self) -> list[str]:
        if not self.should_refresh_cache("models"):
            return self._shared_cache["models"].models

        models = await self.qualifier_service.get_available_models()
        expiration_time = int(time()) + self._cache_expiration_time_seconds
        self._shared_cache = {
            "models": ModelsResponse(models=models, expiration_time=expiration_time)
        }
        return models

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
