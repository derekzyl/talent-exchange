
from typing import Optional, TypedDict
from datetime import datetime

from app.config.config import Enum
class ReviewRatingEnum(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class ReviewT(TypedDict):
    id: str
    reviewer_id: str
    reviewee_id: str
    skill_share_id: str
    rating: ReviewRatingEnum
    comment: str
    created_at: datetime
    updated_at: Optional[datetime]

class CreateReviewT(TypedDict):
    reviewer_id: str
    reviewee_id: str
    skill_share_id: str
    rating: ReviewRatingEnum
    comment: str
