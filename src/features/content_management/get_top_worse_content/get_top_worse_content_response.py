from pydantic import BaseModel


class TopWorseContentItem(BaseModel):
    content_id: str
    title: str
    summary: str
    rating: float


class GetTopWorseContentResponse(BaseModel):
    is_success: bool
    message: str
    items: list[TopWorseContentItem] = []
