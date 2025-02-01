from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database.db import get_db

from app.core.skills.services.service_skill import SkillService
from app.core.skills.types.types_skills import CreateNewSkillT, CreateSkillT, enum_skill_level
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import UserT
from app.utils.crud.types_crud import ResponseMessage


# Skill Router
skill_router = APIRouter()

@skill_router.post("/")
async def create_skill(
    skill_data: CreateNewSkillT,
    user_id: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    create_skill:CreateSkillT ={**skill_data, "user_id": user_id['id']}
    
    return await skill_service.create_skill(create_skill)

@skill_router.get("/")
async def get_user_skills(
    user_id: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    return await skill_service.get_user_skills(user_id['id'])
@skill_router.get("/search/all")
async def get_all_skills(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    return await skill_service.get_all_skills()

@skill_router.get("/{skill_id}")
async def get_skill_by_id(
    skill_id: str, user_id: Annotated[UserT, Depends(UserService.get_logged_in_user)], db: Annotated[AsyncSession, Depends(get_db)],
):
    skill_service = SkillService(db)
    return await skill_service.get_one_skill({'id':skill_id})

@skill_router.get("/search/q")
async def search_skills(
    db: Annotated[AsyncSession, Depends(get_db)],
    user:Annotated [UserT, Depends(UserService.get_logged_in_user)],
    skill_name: Optional[str] = None,
    skill_category: Optional[str] = None,
    skill_level: Optional[enum_skill_level] = None,
):
    skill_service = SkillService(db)
    print(skill_name, skill_category, skill_level)
    return await skill_service.search_skills(user_country=user["country"], user_region=user["region"], skill_level=skill_level, skill_name=skill_name, skill_category=skill_category)

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
