from pydantic import BaseModel


class ContentByTopic(BaseModel):
    content_id: str
    title: str
    description: str
    rating: float


class TopicSummary(BaseModel):
    topic: str
    contents: list[ContentByTopic]


class GetRecommendedContentResponse(BaseModel):
    is_success: bool
    message: str
    recommendation: list[TopicSummary]
