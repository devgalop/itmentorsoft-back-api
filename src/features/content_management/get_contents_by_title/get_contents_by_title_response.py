from pydantic import BaseModel

from itmentorsoft_persistence.dto import ResourceContentResponse


class GetContentsByTitleResponse(BaseModel):
    is_success: bool
    message: str
    items: list[ResourceContentResponse] = []
    total: int = 0
