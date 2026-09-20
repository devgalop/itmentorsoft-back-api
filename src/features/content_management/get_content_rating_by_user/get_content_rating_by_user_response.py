from pydantic import BaseModel


class RatingDetail(BaseModel):
    content_id: str
    title: str
    summary: str
    rating: float
    student_id: str


class GetContentRatingByUserResponse(BaseModel):
    is_success: bool
    message: str
    rating_detail: RatingDetail | None
