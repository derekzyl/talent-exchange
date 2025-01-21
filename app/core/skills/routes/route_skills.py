from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database.db import get_db

from app.core.skills.services.service_skill import SkillService
from app.core.skills.types.types_skills import CreateSkillT, enum_skill_level
from app.core.users.services.service_user import UserService
from app.utils.crud.types_crud import ResponseMessage


# Skill Router
skill_router = APIRouter()

@skill_router.post("/")
async def create_skill(
    skill_data: CreateSkillT,
    user_id: Annotated[str, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    skill_data.user_id = user_id['id']
    return await skill_service.create_skill(skill_data)

@skill_router.get("/user/{user_id}")
async def get_user_skills(
    user_id: Annotated[str, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    return await skill_service.get_user_skills(user_id)

@skill_router.get("/search")
async def search_skills(
    skill_name: Optional[str] = None,
    skill_category: Optional[str] = None,
    skill_level: Optional[enum_skill_level] = None,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    return await skill_service.search_skills(skill_name, skill_category, skill_level)

@skill_router.get("/category/{category}")
async def get_skills_by_category(
    category: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    return await skill_service.get_skills_by_category(category)

@skill_router.delete("/{skill_id}")
async def soft_delete_skill(
    skill_id: str,
    user_id: Annotated[str, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    return await skill_service.soft_delete_skill(skill_id, user_id)
