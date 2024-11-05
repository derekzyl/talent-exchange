import typing
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.db import get_db, session_manager
from app.core.auth.services.service_auth import AuthService
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import (CreateUserD, CreateUserT,
                                            ForgotPasswordT, LoginUserT)
from app.utils.logger import log

auth_router = APIRouter()

@auth_router.post("/signup", name="AUTH API", summary="this api end point is responsible for authenticating the user on the platform ")
async def create_user (data:Annotated[CreateUserT, Body()], db:AsyncSession=Depends(get_db)):
    user = AuthService(db=db)
    create_user = await user.create(data={**data})
    log.logs.info(f' created user {create_user}')
    json=jsonable_encoder(create_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json)


@auth_router.post("/login", name="AUTH API")
async def login_user(data:Annotated[LoginUserT, Body()], db:AsyncSession=Depends(get_db)):
    user = AuthService(db=db)
    login_user = await user.login(data={**data})
    log.logs.info(f' login user {login_user}')
    json=jsonable_encoder(login_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)



@auth_router.post("/logout", name="AUTH API")
async def logout_user(data:Annotated[CreateUserD, Body()], db:AsyncSession=Depends(get_db)):
    user = AuthService(db=db)
    logout_user = await user.logout(data={})
    log.logs.info(f' logout user {logout_user}')
    json=jsonable_encoder(logout_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)



@auth_router.post("/forgot-password", name="AUTH API")
async def forgot_password(data:Annotated[ForgotPasswordT, Body()],background_tasks:BackgroundTasks, db:AsyncSession=Depends(get_db)):
    user = AuthService(db=db)
    forgot_password = await user.forgot_password(data={**data}, background_task=background_tasks)
    log.logs.info(f' forgot password {forgot_password}')
    json=jsonable_encoder(forgot_password)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)
    