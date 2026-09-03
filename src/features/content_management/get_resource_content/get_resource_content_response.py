from pydantic import BaseModel

from itmentorsoft_persistence.dto import ResourceContentResponse


class GetResourceContentResponse(BaseModel):
    is_success: bool
    message: str
    content: ResourceContentResponse | None = None
