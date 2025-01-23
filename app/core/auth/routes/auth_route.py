from tokenize import Token
import typing
from typing import Annotated, TypedDict

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.db import get_db, session_manager
from app.core.auth.services.service_auth import AuthService
from app.core.auth.services.service_token import TokenService
from app.core.auth.types.types_auth import ChangePassWordT
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import (CreateUserD, CreateUserT,
                                            ForgotPasswordT, LoginUserT, UserT)
from app.utils.convert_sqlalchemy_dict import sqlalchemy_obj_to_dict
from app.utils.crud.types_crud import ResponseMessage
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
async def forgot_password(data:Annotated[ForgotPasswordT, Body()],
                          background_tasks:BackgroundTasks, db:AsyncSession=Depends(get_db)):
    user = AuthService(db=db)
    forgot_password = await user.forgot_password(data={**data}, background_task=background_tasks)
    log.logs.info(f' forgot password {forgot_password}')
    json=jsonable_encoder(forgot_password)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)



class reset_pass(TypedDict):
    token:str
    password:str
    
    
    

@auth_router.post("/reset-password", name="AUTH API", summary="Reset user password")
async def reset_password(data: reset_pass, db: AsyncSession = Depends(get_db)):
    user = AuthService(db=db)
    reset_password = await user.reset_password(data=data) # type: ignore
    log.logs.info(f'Password reset: {reset_password}')
    json = jsonable_encoder(reset_password)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)

@auth_router.post("/verify-email", name="AUTH API", summary="Verify user email")
async def verify_email(data: dict, db: AsyncSession = Depends(get_db)):
    user = AuthService(db=db)
    verify_email = await user.verify_email(data=data)
    log.logs.info(f'Email verified: {verify_email}')
    json = jsonable_encoder(verify_email)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)

@auth_router.post("/send-email-verification", name="AUTH API", summary="Send email verification")
async def send_email_verification(data: dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    user = AuthService(db=db)
    send_email_verification = await user.send_email_verification(data=data, background_task=background_tasks)
    log.logs.info(f'Email verification sent: {send_email_verification}')
    json = jsonable_encoder(send_email_verification)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)

@auth_router.post("/change-password", name="AUTH API", summary="Change user password")
async def change_password(data: ChangePassWordT,
 user_id: Annotated[UserT, Depends(UserService.get_logged_in_user)],


                          db: AsyncSession = Depends(get_db)):
    user = AuthService(db=db)
    change_password = await user.change_password(data={**data, 'user_id':user_id['id']})
    log.logs.info(f'Password changed: {change_password}')
    json = jsonable_encoder(change_password)
    return JSONResponse(status_code=status.HTTP_200_OK, content=json)

