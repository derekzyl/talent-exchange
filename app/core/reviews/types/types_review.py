
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
