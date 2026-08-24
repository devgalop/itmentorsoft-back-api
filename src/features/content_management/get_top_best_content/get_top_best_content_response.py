from pydantic import BaseModel


class TopBestContentItem(BaseModel):
    content_id: str
    title: str
    summary: str
    rating: float


class GetTopBestContentResponse(BaseModel):
    is_success: bool
    message: str
    items: list[TopBestContentItem] = []
