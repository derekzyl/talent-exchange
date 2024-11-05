


from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.db import get_db
from app.core.users.services.service_user import UserService

router = APIRouter(
    prefix="/users", tags=['Users'])


@router.get(path="/{user_id}")
async def get_user (  user_id:Annotated[str, Path(title="The ID of the user to get")], db :Annotated[AsyncSession, Depends(get_db) ]):
    user  = await UserService(db=db).get_user_by_id(user_id=user_id)
    return JSONResponse(status_code=200, content=user)



    
    
