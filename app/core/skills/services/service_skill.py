

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
from app.core.skills.types.types_skills  import SkillT, AvailableTimeT, enum_skill_level

class SkillService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=SkillModel, db=db) # type: ignore

    async def get_user_skills(self, user_id: str) -> ResponseMessage:
        """Get all skills for a specific user"""
        query = select(self.model).filter(
            and_(
                self.model.user_id == user_id, # type: ignore
                self.model.deleted_at.is_(None) # type: ignore
            )
        )
        result = await self.db.execute(query)
        skills = result.scalars().all()
        
        return response_message(
            data=skills,
            doc_length=len(skills) if skills else 0,
            message="User skills retrieved successfully",
            success_status=True
        )

    async def search_skills(
        self, 
        skill_name: Optional[str] = None,
        skill_category: Optional[str] = None,
        skill_level: Optional[enum_skill_level] = None
    ) -> ResponseMessage:
        """Search skills based on various criteria"""
        filters = []
        if skill_name:
            filters.append(self.model.skill_name.ilike(f"%{skill_name}%")) # type: ignore
        if skill_category:
            filters.append(self.model.skill_category == skill_category) # type: ignore
        if skill_level:
            filters.append(self.model.skill_level == skill_level) # type: ignore

        query = select(self.model).filter(
            and_(
                *filters,
                self.model.deleted_at.is_(None) # type: ignore
            )
        )
        
        result = await self.db.execute(query)
        skills = result.scalars().all()
        
        return response_message(
            data=skills,
            doc_length=len(skills) if skills else 0,
            message="Skills search completed",
            success_status=True
        )

    async def get_skills_by_category(self, category: str) -> ResponseMessage:
        """Get all skills in a specific category"""
        query = select(self.model).filter(
            and_(
                self.model.skill_category == category, # type: ignore
                self.model.deleted_at.is_(None) # type: ignore
            )
        )
        result = await self.db.execute(query)
        skills = result.scalars().all()
        
        return response_message(
            data=skills,
            doc_length=len(skills) if skills else 0,
            message=f"Skills in category {category} retrieved",
            success_status=True
        )

    async def soft_delete_skill(self, skill_id: str, user_id: str) -> ResponseMessage:
        """Soft delete a skill by setting deleted_at"""
        skill = await self.get_one({"id": skill_id, "user_id": user_id})
        if not skill.get('data'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found"
            )
        
        await self.update(
            filter={"id": skill_id},
            data={"deleted_at": datetime.utcnow()}
        )
        
        return response_message(
            message="Skill soft deleted successfully",
            success_status=True
        )
