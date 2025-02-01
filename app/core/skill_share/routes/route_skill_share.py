# routes/skill_share.py
import re
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.config.database.db import get_db
from app.core.skill_share.services.services_skill_share import SkillShareService
from app.core.skill_share.types.types_skill_share import CreateSkillShareRequestT, IncomingCreateSkillShareRequestT, SkillShareStatusEnum
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import UserT
from app.utils import convert_sqlalchemy_dict
from app.utils.crud.types_crud import ResponseMessage, response_message




# Router groups
skill_share_router = APIRouter()



# Skill Share Request Routes
@skill_share_router.post("/request", response_model=ResponseMessage)
async def create_skill_share_request(
    request_data: IncomingCreateSkillShareRequestT,
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a new skill share request"""
    service = SkillShareService(db)
    request_data["requester_id"] = current_user["id"]
    return await service.create_share_request(request_data)

@skill_share_router.get("/requests/sent", response_model=ResponseMessage)
async def get_sent_requests(
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all skill share requests sent by the current user"""
    service = SkillShareService(db)
    data= await service.get_many(
        query={},
        filter={"requester_id": current_user["id"]}
    )
    if data.get('data') is None:
        raise HTTPException(status_code=404, detail="No requests found")    
    converter = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(data['data'])
    return response_message(
        data=converter,
        message=data.get("message", ""),
        
        doc_length=len(converter) if converter else 0,
        success_status=data.get("success_status", False)
        
    )
@skill_share_router.get("/requests/received", response_model=ResponseMessage)
async def get_received_requests(
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all skill share requests received by the current user"""
    service = SkillShareService(db)
    
    return await service.get_many(
        query={},
        filter={"provider_id": current_user["id"]}
    )

@skill_share_router.patch("/request/{request_id}/status", response_model=ResponseMessage)
async def update_request_status(
    request_id: str,
    new_status: SkillShareStatusEnum,
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Update the status of a skill share request"""
    service = SkillShareService(db)
    return await service.update_share_request_status(
        request_id,
        current_user["id"],
        new_status
    )
