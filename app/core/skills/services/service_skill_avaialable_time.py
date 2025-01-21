

from app.config.database.db import AsyncSession
from app.core.skills.models.model_skills import SkillModel
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import and_, or_, func
from datetime import datetime

from app.config.database.db import AsyncSession
from app.core.skills.models.model_skills import SkillModel
from app.core.skills.models.model_available_time import SkillAvailableTimeModel
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import ResponseMessage, response_message
from app.core.skills.types.types_skills import CreateAvailableTimeT, SkillT, AvailableTimeT, enum_skill_level

class SkillAvailableTimeService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=SkillAvailableTimeModel, db=db) # type: ignore

    async def get_available_times_by_skill(self, skill_id: str) -> ResponseMessage:
        """Get all available times for a specific skill"""
        query = select(self.model).filter(
            and_(
                self.model.skill_id == skill_id, # type: ignore
                self.model.deleted_at.is_(None) # type: ignore
            )
        )
        result = await self.db.execute(query)
        times = result.scalars().all()
        
        return response_message(
            data=times,
            doc_length=len(times) if times else 0,
            message="Available times retrieved successfully",
            success_status=True
        )

    async def get_available_times_by_day(self, day: str) -> ResponseMessage:
        """Get all available times for a specific day"""
        query = select(self.model).filter(
            and_(
                self.model.available_day == day, # type: ignore
                self.model.deleted_at.is_(None) # type: ignore
            )
        )
        result = await self.db.execute(query)
        times = result.scalars().all()
        
        return response_message(
            data=times,
            doc_length=len(times) if times else 0,
            message=f"Available times for {day} retrieved",
            success_status=True
        )

    async def check_time_conflict(
        self, 
        skill_id: str,
        available_day: str,
        start_time: str,
        end_time: str
    ) -> bool:
        """Check if there's a time conflict for a given skill"""
        query = select(self.model).filter(
            and_(
                self.model.skill_id == skill_id, # type: ignore
                self.model.available_day == available_day, # type: ignore
                self.model.deleted_at.is_(None), # type: ignore
                or_(
                    and_(
                        self.model.start_time <= start_time, # type: ignore
                        self.model.end_time > start_time # type: ignore
                    ),
                    and_(
                        self.model.start_time < end_time, # type: ignore
                        self.model.end_time >= end_time # type: ignore
                    )
                )
            )
        )
        result = await self.db.execute(query)
        return bool(result.scalar_one_or_none())

    async def add_available_time(self, data:CreateAvailableTimeT) -> ResponseMessage:
        """Add new available time with conflict checking"""
        has_conflict = await self.check_time_conflict(
            data["skill_id"],
            data["available_day"],
            data["start_time"],
            data["end_time"]
        )
        
        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time slot conflicts with existing availability"
            )
        
        return await self.create(data)

    async def update_available_time(
        self,
        time_id: str,
        data: Dict[str, Any]
    ) -> ResponseMessage:
        """Update available time with conflict checking"""
        if "start_time" in data or "end_time" in data:
            current_time = (await self.get_one({"id": time_id}))['data'] # type: ignore
            if not current_time:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Available time not found"
                )
            
            has_conflict = await self.check_time_conflict(
                current_time.skill_id,
                current_time.available_day,
                data.get("start_time", current_time.start_time),
                data.get("end_time", current_time.end_time)
            )
            
            if has_conflict:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Updated time slot conflicts with existing availability"
                )
        
        return await self.update({"id": time_id}, data)

    async def soft_delete_available_time(self, time_id: str) -> ResponseMessage:
        
        """Soft delete an available time slot"""
        return await self.update(
            filter={"id": time_id},
            data={"deleted_at": datetime.utcnow()}
        )        


    async def create_many_available_time(self, data: List[CreateAvailableTimeT], check:list[dict]|None = None) -> ResponseMessage:
        """Create multiple available times"""
        return await self.create_many(data, check=check)
    