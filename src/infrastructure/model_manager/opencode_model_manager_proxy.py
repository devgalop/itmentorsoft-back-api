from time import time
from dotenv import load_dotenv
import os
from src.features.assessments.shared.qualifier_service import (
    AvailableProcesses,
    ModelExplorerService,
    ModelSelectorService,
)
from src.infrastructure.model_manager.opencode_model_manager import (
    OpencodeModelManagerService,
)

load_dotenv()

OPENCODE_DEFAULT_MODEL = os.getenv("OPENCODE_DEFAULT_MODEL", "")


class AvailableModels:
    def __init__(self, models: list[str], expiration_time: int):
        self.models = models
        self.expiration_time = expiration_time


class OpencodeModelsManagerProxy(ModelExplorerService, ModelSelectorService):

    def __init__(self):
        self._cache_expiration_time_seconds = 14400  # 4 hours
        self._shared_cache: dict[str, AvailableModels] = {}
        self._models_cache: dict[str, str] = {}
        self.models_manager_service = OpencodeModelManagerService()

    async def get_available_models(self) -> list[str]:
        if not self.should_refresh_cache("models"):
            return self._shared_cache["models"].models

        models = await self.models_manager_service.get_available_models()
        expiration_time = int(time()) + self._cache_expiration_time_seconds
        self._shared_cache = {
            "models": AvailableModels(models=models, expiration_time=expiration_time)
        }
        return models

    def get_selected_model(self, process: AvailableProcesses) -> str:
        if process.value in self._models_cache:
            return self._models_cache[process.value]

        # If the selected model is not cached, return the default model
        self._models_cache[process.value] = OPENCODE_DEFAULT_MODEL
        return OPENCODE_DEFAULT_MODEL

    async def set_selected_model(self, process: AvailableProcesses, model_name: str):
        models = await self.get_available_models()
        if model_name not in models:
            raise ValueError(f"Model '{model_name}' is not available.")
        self._models_cache[process.value] = model_name

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
