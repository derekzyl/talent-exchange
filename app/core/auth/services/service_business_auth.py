

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import env
from app.config.config import TokenType
from app.core.auth.services.service_token import (generate_auth_token,
                                                  generate_otp_token,
                                                  generate_token,
                                                  verify_otp_token)
from app.core.auth.types.types_auth import ChangePassWordT, LoginT
from app.core.notification.service.mailer import Mailer
from app.core.users.models.model_user import UserModel
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import CreateUserT, UserT
from app.utils import password_hash
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import response_message
from app.utils.logger.log import logs
from app.utils.regex import email_regex, password_regex


class BusinessAuthService(UserService):
    def __init__(self, db:AsyncSession) -> None:
        super().__init__(db)
        self.db = db
    async def create(self, data:CreateUserT):
        password = password_hash.PassHash().hash_me(data['password'])
        if not password_regex.match(data["password"]):
            raise HTTPException(status_code=400, detail=response_message(error="invalid password", success_status=False, message="password must be 8 character long with uppercase lowercase number and special character"))
        if not email_regex.match(data["email"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_message(error="email is not valid", success_status=False, message="email not valid kindly check your email and retry"))
        #check if the user does exist

        user = select(UserModel).filter(UserModel.email == data["email"])

        result =(await  self.db.scalars(user)).one_or_none()
        if result:# type: ignore

            raise HTTPException(status_code=400, detail=response_message(error="user already exist", success_status=False, message="user already exist kindly login to continue"))

        del data["password"] # type: ignore
        user = await self.create_user(data={"password": password, **data})
        if user["data"] is None: # type: ignore
            raise HTTPException(status_code=400, detail=response_message(error="user not created", success_status=False, message="User not created"))    

        