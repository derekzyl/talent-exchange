from datetime import datetime


from app.config.database.db import AsyncSession
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

class OngoingSkillShareService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=OngoingSkillShareModel, db=db) # type: ignore

    async def create_ongoing_share(
        self,
        skill_share_id: str,
        start_date: datetime,
        end_date: datetime,
        notes: Optional[str] = None
    ) -> ResponseMessage:
        # Verify skill share exists and is accepted
        share_service = SkillShareService(self.db)
        share = await share_service.get_one({
            "id": skill_share_id,
            "status": SkillShareStatusEnum.ACCEPTED.value
        })

        if not share.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only create ongoing share for accepted requests"
            )

        data = {
            "skill_share_id": skill_share_id,
            "start_date": start_date,
            "end_date": end_date,
            "status": SkillShareStatusEnum.ACCEPTED,
            "notes": notes
        }

        return await self.create(data)