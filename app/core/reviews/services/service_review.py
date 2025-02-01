from datetime import datetime


from app.config.database.db import AsyncSession
from app.core.reviews.model.model_reviews import ReviewModel
from app.core.reviews.types.types_review import CreateReviewT
from app.core.skill_share.model.ongoing_share_model import OngoingSkillShareModel
from app.core.skill_share.services.services_skill_share import SkillShareService
from app.core.skill_share.types.types_skill_share import SkillShareStatusEnum
from app.core.skills.models.model_skills import SkillModel
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import and_, or_, func
from datetime import datetime

from app.config.database.db import AsyncSession
from app.core.skills.models.model_skills import SkillModel
from app.core.skills.models.model_available_time import SkillAvailableTimeModel
from app.core.skills.services.service_skill_avaialable_time import SkillAvailableTimeService
from app.utils import convert_sqlalchemy_dict
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import ResponseMessage, response_message
from app.core.skills.types.types_skills  import CreateSkillT, CreateTimeT, SkillT, AvailableTimeT, enum_skill_level

class ReviewService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=ReviewModel, db=db) # type: ignore

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

        rev =  await self.create(data) # type: ignore

        data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(rev['data']) # type: ignore
        return response_message(
            data=data,
            message=rev.get("message", ""),
            success_status=rev.get("success_status", False)
        )
