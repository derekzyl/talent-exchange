


from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.db import get_db
from app.core.users.services.service_user import UserService

user_router = APIRouter(
    prefix="/users", tags=['Users'])


@user_router.get(path="/profile ", name="Get User Profile", summary="Get User Profile")
async def get_user (  user_id:Annotated[str, Depends(UserService.get_logged_in_user)], db :Annotated[AsyncSession, Depends(get_db) ]):
    # user  = await UserService(db=db).get_user_by_id(user_id=user_id)
    return JSONResponse(status_code=200, content=user_id)



    
    
