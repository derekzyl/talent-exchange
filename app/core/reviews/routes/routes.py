from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.config.database.db import get_db
from app.core.auth.services.middleware_auth import response_message
from app.core.reviews.services.service_review import ReviewService
from app.core.reviews.types.types_review import CreateReviewT
from app.core.skill_share.services.service_exhange import OngoingSkillShareService
from app.core.skill_share.services.services_skill_share import SkillShareService
from app.core.skill_share.types.types_skill_share import SkillShareStatusEnum
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import UserT
from app.utils import convert_sqlalchemy_dict
from app.utils.crud.types_crud import ResponseMessage
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
    re= await service.get_many(
        query={},
        filter={"reviewee_id": user_id}
    )
    return response_message(
        data=convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(re.get('data', [])),
        message=re.get("message", ""),
        doc_length=len(re.get('data', [])),
        success_status=re.get("success_status", False)
    )

@review_router.get("/share/{share_id}", response_model=ResponseMessage)
async def get_share_reviews(
    share_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all reviews for a specific skill share"""
    service = ReviewService(db)
    re = await service.get_many(
        query={},
        filter={"skill_share_id": share_id}
    )
    return response_message(
        data=convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(re.get('data', [])),
        message=re.get("message", ""),
        doc_length=len(re.get('data', [])),
        success_status=re.get("success_status", False)
    )
