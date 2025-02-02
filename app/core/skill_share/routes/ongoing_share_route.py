from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import or_, select
from app.config.database.db import get_db
import app.core.skill_share.services.service_exchange.service_exhange as OngoingSkillShareService

from app.core.skill_share.types.enum_skills import SkillShareStatusEnum
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import UserT
from app.utils import convert_sqlalchemy_dict
from app.utils.crud.types_crud import ResponseMessage


ongoing_share_router = APIRouter()


# # Ongoing Skill Share Routes
# @ongoing_share_router.post("", response_model=ResponseMessage)
# async def create_ongoing_share(
#     share_id: str,
#     start_date: datetime,
#     end_date: datetime,
#     current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
#     db: Annotated[AsyncSession, Depends(get_db)],
#     notes: Optional[str] = None
# ):
#     """Create a new ongoing skill share session"""
#     service = OngoingSkillShareService.OngoingSkillShareService(db)
#     return await service.create_ongoing_share(
#         share_id,
#         start_date,
#         end_date,
#         notes
#     )

@ongoing_share_router.get("/active", response_model=ResponseMessage)
async def get_active_shares(
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all active ongoing skill shares for the current user using SQLAlchemy's or_ operator."""
    
    # Build the query directly using SQLAlchemy.
    from app.core.skill_share.model.skill_share_model import SkillShareRequestModel
    query = select(SkillShareRequestModel).where(
        SkillShareRequestModel.status == SkillShareStatusEnum.ACCEPTED.value,
        or_(
            SkillShareRequestModel.requester_id == current_user["id"],
            SkillShareRequestModel.provider_id == current_user["id"]
        )
    )
    
    # Execute the query.
    result = await db.execute(query)
    user_shares = result.scalars().all()
    
    # Return an appropriate response.
    if not user_shares:
        return ResponseMessage(
            data=[],
            message="No active shares found",
            success_status=True,
            doc_length=0
        )
    
    # If needed, convert the SQLAlchemy objects to dicts or your desired response model.
    shares_as_dict = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(user_shares)
    
    shares_list = shares_as_dict if isinstance(shares_as_dict, list) else [shares_as_dict]
    return ResponseMessage(
        data=shares_as_dict,
        message="Active shares retrieved successfully",
        success_status=True,
        doc_length=len(shares_list)
    )
@ongoing_share_router.patch("/{share_id}/complete", response_model=ResponseMessage)
async def complete_ongoing_share(
    share_id: str,
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Mark an ongoing skill share as completed"""
    ongoing_service = OngoingSkillShareService.OngoingSkillShareService(db)
    from app.core.skill_share.services.skill_share.s_skill_share import SkillShareService
    share_service = SkillShareService(db)
    
    # Verify the ongoing share exists and user is involved
    ongoing_share = await ongoing_service.get_one({"id": share_id})
    if not ongoing_share.get("data"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ongoing share not found"
        )
    
    # Get the original share request to verify user permission
    ongoing_share_data = ongoing_share.get("data")
    if not ongoing_share_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ongoing share data not found"
        )
    
    original_share = await share_service.get_one({
        "id": ongoing_share_data["skill_share_id"]
    })
    
    if not original_share.get("data"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Original share request not found"
        )
    
    if ("data" not in original_share or 
        original_share["data"]["requester_id"] != current_user["id"] and 
        original_share["data"]["provider_id"] != current_user["id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to complete this share"
        )
    
    # Update both ongoing share and original share request status
    await ongoing_service.update(
        filter={"id": share_id},
        data={"status": SkillShareStatusEnum.COMPLETED.value}
    )
    
    return await share_service.update(
        filter={"id": ongoing_share_data["skill_share_id"]},
        data={"status": SkillShareStatusEnum.COMPLETED.value}
    )
