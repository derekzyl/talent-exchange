

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
from app.core.skills.services.service_skill_avaialable_time import SkillAvailableTimeService
from app.core.users.models.model_user import UserModel
from app.utils import convert_sqlalchemy_dict
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import ResponseMessage, response_message
from app.core.skills.types.types_skills  import CreateSkillT, CreateTimeT, SkillT, AvailableTimeT, enum_skill_level

class SkillService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=SkillModel, db=db) # type: ignore


    async def create_skill(self, data: CreateSkillT ) -> ResponseMessage:
         

        #  check if the skill already exists for the user 

        skill = await self.get_one({"skill_name": data['skill_name'], "user_id": data['user_id']})
        if skill.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ResponseMessage({
                    "error": "Skill already exists",
                    "message": "Skill already exists for the user",
                    "success_status": False
                    
                }))
            
        skill_data = {
            "skill_name": data['skill_name'],
            "skill_category": data['skill_category'],
            "skill_level": data['skill_level'].value,
            "user_id": data['user_id'],
            "skill_description": data['skill_description'],
            
        }
        skill = await self.create(data=skill_data)
        if "available_time" in data and data['available_time'] and 'data' in skill:
            skill_time:list[CreateTimeT]  = data.pop('available_time', None)
                  
                       #  create available days 
            new_data:list[dict] = []
            available_time_service = SkillAvailableTimeService(self.db)

            for time in skill_time:
                new_data.append({
                    "available_day": time['available_day'],
                    "start_time": time['start_time'],
                    "end_time": time['end_time'],
                    "skill_id": skill['data']['id']
                })

            await available_time_service.add_available_time(data=new_data)   
        return response_message(
            data=skill,
            message="Skill created successfully",
            success_status=True
        )   

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
    async def get_all_skills(self) -> ResponseMessage:
        """Get all skills"""
        query = select(self.model).filter(
            self.model.deleted_at.is_(None) # type: ignore
        )
        result = await self.db.execute(query)
        skills = result.scalars().all()

        converter = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(skills)
        
        return response_message(
            data=converter,
            doc_length=len(converter) if converter else 0,
            message="All skills retrieved successfully",
            success_status=True
        )

    async def get_one_skill(self, filter: Dict[str, Any]) -> ResponseMessage:
        try:
            """Get a single skill based on a filter"""
            
      
            result = await self.get_one(filter)

            if 'data' not in result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Skill not found"
                )

            convert_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(result['data'])
           
            
            return response_message(
                data=convert_data,
                message="Skill retrieved successfully",
                success_status=True,
                doc_length=1
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )





    async def search_skills(
        self,
        user_country: str,
        user_region: str,
        skill_name: Optional[str] = None,
        skill_category: Optional[str] = None,
        skill_level: Optional[enum_skill_level] = None
    ) -> ResponseMessage:
        filters = [
            self.model.deleted_at.is_(None), # type: ignore
            UserModel.country == user_country,
            UserModel.region == user_region
        ]
        
        if skill_name:
            filters.append(self.model.skill_name.ilike(f"%{skill_name}%")) # type: ignore
        if skill_category:
            filters.append(self.model.skill_category == skill_category) # type: ignore
        if skill_level:
            filters.append(self.model.skill_level == skill_level.value) # type: ignore

        query = (
            select(self.model)
            .join(UserModel, self.model.user_id == UserModel.id) # type: ignore
            .filter(and_(*filters))
        )
        
        result = await self.db.execute(query)
        skills = result.scalars().all()
        
        return response_message(
            data=skills,
            doc_length=len(skills),
            success_status=True,
            message="Skills search completed"
            
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
