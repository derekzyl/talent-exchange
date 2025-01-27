

from app.config.database.db import AsyncSession
from app.core.skill_share.model.skill_share_model import SkillShareRequestModel
from app.core.skill_share.types.types_skill_share import CreateSkillShareRequestT, SkillShareStatusEnum
from app.core.skills.models.model_skills import SkillModel
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import and_, or_, func
from datetime import datetime

from app.config.database.db import AsyncSession
from app.core.skills.models.model_skills import SkillModel
from app.core.skills.models.model_available_time import SkillAvailableTimeModel
from app.core.skills.services.service_skill import SkillService
from app.core.skills.services.service_skill_avaialable_time import SkillAvailableTimeService
from app.utils import convert_sqlalchemy_dict
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import ResponseMessage, response_message
from app.core.skills.types.types_skills  import CreateSkillT, CreateTimeT, SkillT, AvailableTimeT, enum_skill_level


class SkillShareService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=SkillShareRequestModel, db=db) # type: ignore

    async def create_share_request(self, data: CreateSkillShareRequestT) -> ResponseMessage:
        # Verify users and skills exist
        if data['requester_id'] == data['provider_id']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot request skill share with yourself"
            )

        # Check for existing pending requests
        existing_request = await self.get_one({
            "requester_id": data['requester_id'],
            "provider_id": data['provider_id'],
            "requester_skill_id": data['requester_skill_id'],
            "provider_skill_id": data['provider_skill_id'],
            "status": SkillShareStatusEnum.PENDING.value
        })

        if existing_request.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A pending request already exists"
            )

        skills = SkillService(self.db)   
        requester_skill = await skills.get_one({"user_id": data['requester_skill_id']})
        provider_skill = await skills.get_one({"user_id": data['provider_skill_id']})
        
        

         
        skill_user =await  self.create(data) # type: ignore
        converter = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(skill_user)

        return  response_message(
            data=converter,
            message="Skill share request created successfully",
            success_status=True
        )

    async def update_share_request_status(
        self,
        request_id: str,
        user_id: str,
        new_status: SkillShareStatusEnum
    ) -> ResponseMessage:
        request = await self.get_one({"id": request_id})
        if not request.get('data'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Share request not found"
            )

        if 'data' not in request or request['data'] is None or request['data'].provider_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the provider can update the request status"
            )

        return await self.update(
            filter={"id": request_id},
            data={"status": new_status.value}
        )
