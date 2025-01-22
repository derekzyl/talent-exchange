
review_router = APIRouter()


# Review Routes
@review_router.post("", response_model=ResponseMessage)
async def create_review(
    review_data: CreateReviewT,
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a new review for a completed skill share"""
    service = ReviewService(db)
    review_data["reviewer_id"] = current_user["id"]
    return await service.create_review(review_data)

@review_router.get("/user/{user_id}", response_model=ResponseMessage)
async def get_user_reviews(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all reviews for a specific user"""
    service = ReviewService(db)
    return await service.get_many(
        query={},
        filter={"reviewee_id": user_id}
    )

@review_router.get("/share/{share_id}", response_model=ResponseMessage)
async def get_share_reviews(
    share_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all reviews for a specific skill share"""
    service = ReviewService(db)
    return await service.get_many(
        query={},
        filter={"skill_share_id": share_id}
    )
