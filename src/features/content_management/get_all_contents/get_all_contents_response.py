from pydantic import BaseModel

from itmentorsoft_persistence.dto import ResourceContentResponse


class GetAllContentsResponse(BaseModel):
    is_success: bool
    message: str
    items: list[ResourceContentResponse] = []
    total: int = 0

    model_config = {"arbitrary_types_allowed": True}
