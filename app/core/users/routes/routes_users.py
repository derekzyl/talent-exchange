from typing import Annotated, List
from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.db import get_db
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import CreateUserT, UpdateUserT

user_router = APIRouter()

@user_router.post("/", response_model=dict)
async def create_user(
    data: CreateUserT,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await UserService(db=db).create_user(data=data)
    return JSONResponse(status_code=201, content=user)

@user_router.get("/profile")
async def get_profile(
    user_id: Annotated[str, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return JSONResponse(status_code=200, content=user_id)

@user_router.get("/{user_id}")
async def get_user_by_id(
    user_id: Annotated[str, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await UserService(db=db).get_user_by_id(user_id=user_id)
    return JSONResponse(status_code=200, content=user)

@user_router.get("/country/{country}")
async def get_users_by_country(
    country: Annotated[str, Path()],
    db: Annotated[AsyncSession, Depends(get_db)],
    select: List[str] = Query(None)
):
    filter = {"select": select} if select else None
    users = await UserService(db=db).get_users_by_country(country=country, filter=filter)
    return JSONResponse(status_code=200, content=users)

@user_router.put("/{user_id}")
async def update_user(
    user_id: Annotated[str, Path()],
    data: UpdateUserT,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await UserService(db=db).update_user(filter={"id": user_id}, data=data)
    return JSONResponse(status_code=200, content=user)

@user_router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[str, Path()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await UserService(db=db).delete_user(user_id=user_id)
    return JSONResponse(status_code=204,    content={"message": "User deleted successfully"})