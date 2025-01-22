
class ReviewService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=ReviewModel, db=db)

    async def create_review(self, data: CreateReviewT) -> ResponseMessage:
        # Verify the skill share exists and is completed
        share_service = SkillShareService(self.db)
        share = await share_service.get_one({
            "id": data['skill_share_id'],
            "status": SkillShareStatusEnum.COMPLETED
        })

        if not share.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only review completed skill shares"
            )

        # Check if review already exists
        existing_review = await self.get_one({
            "reviewer_id": data['reviewer_id'],
            "skill_share_id": data['skill_share_id']
        })

        if existing_review.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review already exists"
            )

        return await self.create(data)
