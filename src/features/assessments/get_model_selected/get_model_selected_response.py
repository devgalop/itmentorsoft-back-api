from pydantic import BaseModel


class ModelByProcess(BaseModel):
    process: str
    model_id: str


class GetModelSelectedResponse(BaseModel):
    is_success: bool
    message: str
    models_by_process: list[ModelByProcess]
