from pydantic import BaseModel


class GetAvailableModelsResponse(BaseModel):
    is_success: bool
    message: str
    models: list[str] = []
