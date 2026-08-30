import asyncio
from dotenv import load_dotenv
import os
from openai import OpenAI

from src.features.assessments.shared.qualifier_service import ModelExplorerService

load_dotenv()

OPENCODE_API_KEY = os.getenv("OPENCODE_API_KEY", "")
OPENCODE_API_URL = os.getenv("OPENCODE_API_URL", "")


class OpencodeModelManagerService(ModelExplorerService):

    def __init__(self):
        self.client = OpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_API_URL)

    async def get_available_models(self) -> list[str]:
        try:
            response = await asyncio.to_thread(self.client.models.list)
            models = [model.id for model in response.data]
            return models
        except Exception:
            return []
